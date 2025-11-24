#!/usr/bin/env python3
"""
プロジェクト分析スクリプト

このスクリプトは以下を分析し、実行すべきアクションを返します:
- 初回セットアップの完了状況
- PRの状態（レビュー待ち、マージ可能、未作成）
- Issueの優先順位
- 停滞タスク
- CI/CDの健全性
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any


def run_command(cmd: str) -> Dict[str, Any]:
    """コマンドを実行して結果を返す"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def check_initial_setup() -> Dict[str, Any]:
    """初回セットアップの完了状況を確認"""
    # マイルストーン数（オープンとクローズ両方）
    all_milestones = run_command("gh api repos/:owner/:repo/milestones?state=all | jq 'length'")
    labels = run_command("gh label list | grep -c 'priority:' || true")

    milestone_count = int(all_milestones["stdout"]) if all_milestones["success"] else 0
    label_count = int(labels["stdout"]) if labels["success"] else 0

    needs_setup = milestone_count < 5 or label_count < 4

    return {
        "needs_setup": needs_setup,
        "milestone_count": milestone_count,
        "label_count": label_count
    }


def check_prs() -> Dict[str, Any]:
    """PR状態を確認"""
    # オープンなPR
    open_prs = run_command("gh pr list --state open --json number,title,isDraft,reviewDecision,statusCheckRollup,headRefName")
    prs = json.loads(open_prs["stdout"]) if open_prs["success"] else []

    # PRが必要なブランチ
    run_command("git fetch origin")
    branches_result = run_command("git branch -r | grep -v 'HEAD\\|master\\|main\\|develop' || true")
    branches = [b.strip().replace("origin/", "") for b in branches_result["stdout"].split("\n") if b.strip()]

    branches_without_pr = []
    for branch in branches:
        pr_check = run_command(f"gh pr list --state all --head {branch} --json number")
        pr_list = json.loads(pr_check["stdout"]) if pr_check["success"] else []
        if not pr_list:
            branches_without_pr.append(branch)

    # PRを分類
    ready_to_merge = []
    needs_review = []
    draft_prs = []
    draft_issues = set()  # Draft PRが存在するIssue番号

    for pr in prs:
        if pr.get("isDraft"):
            draft_prs.append(pr)
            # Issue番号を抽出（ブランチ名から）
            branch = pr.get("headRefName", "")
            if "issue-" in branch:
                issue_num = branch.split("issue-")[1].split("-")[0]
                draft_issues.add(issue_num)
        elif pr.get("reviewDecision") == "APPROVED" and pr.get("statusCheckRollup", {}).get("state") == "SUCCESS":
            ready_to_merge.append(pr)
        else:
            needs_review.append(pr)

    return {
        "branches_without_pr": branches_without_pr,
        "ready_to_merge": ready_to_merge,
        "needs_review": needs_review,
        "draft_prs": draft_prs,
        "draft_issues": list(draft_issues)
    }


def check_issues() -> Dict[str, Any]:
    """Issue優先順位を確認"""
    critical = run_command("gh issue list --label 'priority:critical' --json number,title,milestone")
    bugs = run_command("gh issue list --label 'bug' --json number,title,milestone")
    all_open = run_command("gh issue list --state open --json number,title,labels,milestone")

    critical_issues = json.loads(critical["stdout"]) if critical["success"] else []
    bug_issues = json.loads(bugs["stdout"]) if bugs["success"] else []
    all_issues = json.loads(all_open["stdout"]) if all_open["success"] else []

    # マイルストーンなしのIssue
    no_milestone = [i for i in all_issues if not i.get("milestone")]

    return {
        "critical_issues": critical_issues,
        "bug_issues": bug_issues,
        "no_milestone_issues": no_milestone[:5]  # 最大5件
    }


def check_stagnant_tasks() -> Dict[str, Any]:
    """停滞タスクを確認"""
    # 48時間以上更新されていないDraft PR
    cutoff_date = (datetime.now() - timedelta(hours=48)).isoformat()
    stagnant_drafts = run_command(
        f"gh pr list --state open --draft --json number,title,updatedAt | "
        f"jq '[.[] | select(.updatedAt < \"{cutoff_date}\")]'"
    )

    stagnant = json.loads(stagnant_drafts["stdout"]) if stagnant_drafts["success"] else []

    return {
        "stagnant_draft_prs": stagnant
    }


def check_ci_health() -> Dict[str, Any]:
    """CI/CD健全性を確認"""
    recent_runs = run_command("gh run list --limit 10 --json conclusion,status")
    runs = json.loads(recent_runs["stdout"]) if recent_runs["success"] else []

    failed_runs = [r for r in runs if r.get("conclusion") == "failure"]

    return {
        "recent_failures": len(failed_runs),
        "has_failures": len(failed_runs) > 0
    }


def generate_actions(analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """分析結果から実行すべきアクションを生成"""
    actions = []

    # Critical: 初回セットアップ
    if analysis["setup"]["needs_setup"]:
        actions.append({
            "priority": "CRITICAL",
            "action": "initial_setup",
            "description": f"初回セットアップを実行（マイルストーン: {analysis['setup']['milestone_count']}/5, ラベル: {analysis['setup']['label_count']}/4）",
            "instructions": [
                "1. `cat .github/templates/project-setup.md` を実行してプロジェクト要件を読む",
                "2. 不足しているリソースを作成:",
                "   - GitHubプロジェクト（存在しない場合）",
                "   - マイルストーン（5件必要）",
                "   - 優先度ラベル（priority:critical/high/medium/low）",
                "   - カテゴリラベル（feature/bug/documentation等）",
                "   - 各マイルストーンの初期Issue",
                "3. 完了報告をこのIssueに投稿"
            ]
        })
        return actions  # セットアップが必要な場合は他の処理をスキップ

    draft_issues = set(analysis["prs"]["draft_issues"])

    # Critical: バグとCriticalなIssue（Draft PRがないもののみ）
    if analysis["issues"]["critical_issues"]:
        for issue in analysis["issues"]["critical_issues"][:3]:
            issue_num = str(issue['number'])
            if issue_num in draft_issues:
                continue  # Draft PR存在するのでスキップ

            actions.append({
                "priority": "CRITICAL",
                "action": "implement_critical_issue",
                "issue_number": issue['number'],
                "description": f"Critical Issue #{issue['number']} を実装: {issue['title']}",
                "instructions": [
                    f"⚠️ 必須: 以下の順序で作業してください:",
                    f"",
                    f"1. ブランチを作成:",
                    f"   git checkout -b feature/issue-{issue['number']}-{issue['title'][:20].replace(' ', '-').lower()}",
                    f"",
                    f"2. 空コミットでDraft PRを先に作成:",
                    f"   git commit --allow-empty -m 'WIP: Issue #{issue['number']} の実装開始'",
                    f"   git push origin feature/issue-{issue['number']}-{issue['title'][:20].replace(' ', '-').lower()}",
                    f"   gh pr create --draft --title 'WIP: Issue #{issue['number']} {issue['title']}' --body 'Issue #{issue['number']} の実装を進めています。Closes #{issue['number']}' --base develop",
                    f"",
                    f"3. 実装を進める:",
                    f"   - コードを書く",
                    f"   - テストを追加",
                    f"   - コミット・プッシュを繰り返す",
                    f"",
                    f"4. 実装完了後、Draft を解除:",
                    f"   gh pr ready",
                    f"",
                    f"5. レビュー依頼:",
                    f"   PRにコメントでレビューを依頼"
                ]
            })

    if analysis["issues"]["bug_issues"]:
        for issue in analysis["issues"]["bug_issues"][:2]:
            issue_num = str(issue['number'])
            if issue_num in draft_issues:
                continue

            actions.append({
                "priority": "CRITICAL",
                "action": "fix_bug",
                "issue_number": issue['number'],
                "description": f"Bug #{issue['number']} を修正: {issue['title']}",
                "instructions": [
                    f"⚠️ 必須: 以下の順序で作業してください:",
                    f"",
                    f"1. ブランチを作成:",
                    f"   git checkout -b fix/issue-{issue['number']}-{issue['title'][:20].replace(' ', '-').lower()}",
                    f"",
                    f"2. 空コミットでDraft PRを先に作成:",
                    f"   git commit --allow-empty -m 'WIP: Fix #{issue['number']} の修正開始'",
                    f"   git push origin fix/issue-{issue['number']}-{issue['title'][:20].replace(' ', '-').lower()}",
                    f"   gh pr create --draft --title 'WIP: Fix #{issue['number']} {issue['title']}' --body 'Issue #{issue['number']} のバグ修正を進めています。Fixes #{issue['number']}' --base develop",
                    f"",
                    f"3. バグを修正:",
                    f"   - 原因を特定",
                    f"   - 修正を実装",
                    f"   - テストを追加",
                    f"",
                    f"4. 実装完了後、Draft を解除:",
                    f"   gh pr ready"
                ]
            })

    # High: PR未作成のブランチ
    if analysis["prs"]["branches_without_pr"]:
        for branch in analysis["prs"]["branches_without_pr"][:3]:
            # Issue番号を抽出
            issue_num = None
            if "issue-" in branch:
                issue_num = branch.split("issue-")[1].split("-")[0]

            actions.append({
                "priority": "HIGH",
                "action": "create_pr_for_branch",
                "branch": branch,
                "description": f"ブランチ {branch} のPRを作成",
                "instructions": [
                    f"1. ブランチをチェックアウト:",
                    f"   git fetch origin",
                    f"   git checkout {branch}",
                    f"",
                    f"2. 実装内容を確認:",
                    f"   git log origin/develop..HEAD",
                    f"   git diff origin/develop..HEAD",
                    f"",
                    f"3. PRを作成:",
                    f"   gh pr create --title 'PR for {branch}' --body 'Closes #{issue_num if issue_num else 'TBD'}' --base develop",
                    f"",
                    f"4. 実装が未完了ならDraftに設定:",
                    f"   gh pr ready --undo  # Draft化"
                ]
            })

    # High: マージ可能なPR
    if analysis["prs"]["ready_to_merge"]:
        for pr in analysis["prs"]["ready_to_merge"][:3]:
            actions.append({
                "priority": "HIGH",
                "action": "merge_pr",
                "pr_number": pr['number'],
                "description": f"PR #{pr['number']} をマージ: {pr['title']}",
                "instructions": [
                    f"1. 最終確認:",
                    f"   gh pr view {pr['number']}",
                    f"   gh pr checks {pr['number']}",
                    f"",
                    f"2. マージ実行:",
                    f"   gh pr merge {pr['number']} --squash --delete-branch",
                    f"",
                    f"3. マージ後確認:",
                    f"   git checkout develop",
                    f"   git pull origin develop"
                ]
            })

    # High: レビュー待ちPR
    if analysis["prs"]["needs_review"]:
        for pr in analysis["prs"]["needs_review"][:2]:
            actions.append({
                "priority": "HIGH",
                "action": "review_pr",
                "pr_number": pr['number'],
                "description": f"PR #{pr['number']} をレビュー: {pr['title']}",
                "instructions": [
                    f"1. PRの内容を確認:",
                    f"   gh pr view {pr['number']} --comments",
                    f"   gh pr diff {pr['number']}",
                    f"",
                    f"2. コードレビュー:",
                    f"   - 実装の正しさを確認",
                    f"   - テストカバレッジを確認",
                    f"   - コードスタイルを確認",
                    f"",
                    f"3. レビュー結果を投稿:",
                    f"   gh pr review {pr['number']} --approve -b 'LGTM!'",
                    f"   または",
                    f"   gh pr review {pr['number']} --request-changes -b '修正が必要です: ...'",
                    f"   または",
                    f"   gh pr review {pr['number']} --comment -b 'コメント: ...'"
                ]
            })

    # High: 停滞タスク
    if analysis["stagnant"]["stagnant_draft_prs"]:
        for pr in analysis["stagnant"]["stagnant_draft_prs"][:2]:
            actions.append({
                "priority": "HIGH",
                "action": "revive_stagnant_pr",
                "pr_number": pr['number'],
                "description": f"停滞中のDraft PR #{pr['number']} を再開: {pr['title']}",
                "instructions": [
                    f"1. PRの状態を確認:",
                    f"   gh pr view {pr['number']} --comments",
                    f"",
                    f"2. @claudeメンションで再開を促す:",
                    f"   gh pr comment {pr['number']} --body '@claude このDraft PRが48時間以上更新されていません。実装を継続してください。ブロッカーがあればコメントしてください。'",
                    f"",
                    f"または自分で実装を継続:",
                    f"   git fetch origin",
                    f"   git checkout {pr.get('headRefName', 'branch-name')}",
                    f"   # 実装を継続..."
                ]
            })

    # Medium: マイルストーン未割当てIssue
    if analysis["issues"]["no_milestone_issues"]:
        actions.append({
            "priority": "MEDIUM",
            "action": "assign_milestones",
            "description": f"マイルストーン未割当てIssue {len(analysis['issues']['no_milestone_issues'])}件に割り当て",
            "instructions": [
                "1. マイルストーン一覧を確認:",
                "   gh api repos/:owner/:repo/milestones",
                "",
                "2. 各Issueに適切なマイルストーンを割り当て:",
            ] + [
                f"   gh issue edit {issue['number']} --milestone 'マイルストーン名'  # Issue #{issue['number']}: {issue['title']}"
                for issue in analysis["issues"]["no_milestone_issues"]
            ]
        })

    # Medium: CI失敗
    if analysis["ci"]["has_failures"]:
        actions.append({
            "priority": "MEDIUM",
            "action": "fix_ci",
            "description": f"CI失敗を修正（直近10件中{analysis['ci']['recent_failures']}件失敗）",
            "instructions": [
                "1. 失敗したワークフローを確認:",
                "   gh run list --limit 10",
                "",
                "2. 失敗の詳細を確認:",
                "   gh run view <run-id>",
                "",
                "3. 原因を特定して修正:",
                "   - テスト失敗の場合: テストを修正",
                "   - ビルド失敗の場合: ビルド設定を修正",
                "   - リンターエラーの場合: コードスタイルを修正",
                "",
                "4. 修正をコミット・プッシュ"
            ]
        })

    return actions


def main():
    """メイン処理"""
    print("🔍 プロジェクト分析を開始...")
    print()

    # 各項目を分析
    analysis = {
        "setup": check_initial_setup(),
        "prs": check_prs(),
        "issues": check_issues(),
        "stagnant": check_stagnant_tasks(),
        "ci": check_ci_health()
    }

    # アクションを生成
    actions = generate_actions(analysis)

    if not actions:
        print("✅ アクションは必要ありません。プロジェクトは良好な状態です。")
        return

    print(f"📋 実行すべきアクション: {len(actions)}件\n")
    print("=" * 80)

    for i, action in enumerate(actions, 1):
        print(f"\n【アクション {i}】[{action['priority']}] {action['description']}")
        print("-" * 80)
        if "instructions" in action:
            for instruction in action["instructions"]:
                print(instruction)
        print()

    print("=" * 80)
    print("\n⚠️  重要な注意事項:")
    print("- Issue実装時は必ずDraft PRを先に作成してください")
    print("- Draft PRが存在するIssueには着手しないでください")
    print("- 優先順位（CRITICAL > HIGH > MEDIUM > LOW）の順に実行してください")
    print("- 少なくとも1つのアクションを完了してください")


if __name__ == "__main__":
    main()
