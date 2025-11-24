#!/usr/bin/env python3
"""
完全自動化開発サイクル - プロジェクト分析スクリプト

このスクリプトは以下を分析し、実行すべきアクションを返します:
- 初回セットアップの完了状況
- PRの状態（レビュー待ち、マージ可能、未作成）
- マージ済みPRの品質チェック（バグ検出、改善提案）
- Issueの優先順位と動的更新
- マイルストーン進行管理
- プロジェクトボード自動更新
- 停滞タスク検出
- CI/CDの健全性
- ドキュメント更新必要性
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Set


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
    all_milestones = run_command("gh api repos/:owner/:repo/milestones?state=all | jq 'length'")
    labels = run_command("gh label list | grep -c 'priority:' || true")
    project = run_command("gh project list --owner @me --format json")

    milestone_count = int(all_milestones["stdout"]) if all_milestones["success"] else 0
    label_count = int(labels["stdout"]) if labels["success"] else 0

    projects = json.loads(project["stdout"]) if project["success"] else {"projects": []}
    has_project = len(projects.get("projects", [])) > 0

    needs_setup = milestone_count < 5 or label_count < 4 or not has_project

    return {
        "needs_setup": needs_setup,
        "milestone_count": milestone_count,
        "label_count": label_count,
        "has_project": has_project
    }


def check_prs() -> Dict[str, Any]:
    """PR状態を確認"""
    open_prs = run_command("gh pr list --state open --json number,title,isDraft,reviewDecision,statusCheckRollup,headRefName")
    prs = json.loads(open_prs["stdout"]) if open_prs["success"] else []

    run_command("git fetch origin")
    branches_result = run_command("git branch -r | grep -v 'HEAD\\|master\\|main\\|develop' || true")
    branches = [b.strip().replace("origin/", "") for b in branches_result["stdout"].split("\n") if b.strip()]

    branches_without_pr = []
    for branch in branches:
        pr_check = run_command(f"gh pr list --state all --head {branch} --json number")
        pr_list = json.loads(pr_check["stdout"]) if pr_check["success"] else []
        if not pr_list:
            branches_without_pr.append(branch)

    ready_to_merge = []
    needs_review = []
    draft_prs = []
    draft_issues: Set[str] = set()

    for pr in prs:
        if pr.get("isDraft"):
            draft_prs.append(pr)
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


def check_merged_prs() -> Dict[str, Any]:
    """最近マージされたPRをチェックして、フォローアップが必要か確認"""
    # 過去7日間にマージされたPR
    cutoff_date = (datetime.now() - timedelta(days=7)).isoformat()
    merged_prs = run_command(
        f"gh pr list --state merged --limit 10 --json number,title,mergedAt,body"
    )

    prs = json.loads(merged_prs["stdout"]) if merged_prs["success"] else []
    recent_merged = [pr for pr in prs if pr.get("mergedAt", "") > cutoff_date]

    return {
        "recent_merged_prs": recent_merged
    }


def check_issues() -> Dict[str, Any]:
    """Issue優先順位を確認"""
    critical = run_command("gh issue list --label 'priority:critical' --json number,title,milestone,createdAt")
    bugs = run_command("gh issue list --label 'bug' --json number,title,milestone,createdAt")
    all_open = run_command("gh issue list --state open --json number,title,labels,milestone,createdAt")

    critical_issues = json.loads(critical["stdout"]) if critical["success"] else []
    bug_issues = json.loads(bugs["stdout"]) if bugs["success"] else []
    all_issues = json.loads(all_open["stdout"]) if all_open["success"] else []

    no_milestone = [i for i in all_issues if not i.get("milestone")]

    # 古いIssue（30日以上経過）
    old_cutoff = (datetime.now() - timedelta(days=30)).isoformat()
    old_issues = [i for i in all_issues if i.get("createdAt", "") < old_cutoff]

    return {
        "critical_issues": critical_issues,
        "bug_issues": bug_issues,
        "no_milestone_issues": no_milestone[:5],
        "old_issues": old_issues[:3]
    }


def check_milestones() -> Dict[str, Any]:
    """マイルストーンの進捗を確認"""
    milestones = run_command("gh api repos/:owner/:repo/milestones?state=open")
    milestone_list = json.loads(milestones["stdout"]) if milestones["success"] else []

    completed_milestones = []
    active_milestones = []

    for ms in milestone_list:
        total = ms.get("open_issues", 0) + ms.get("closed_issues", 0)
        if total > 0:
            completion_rate = ms.get("closed_issues", 0) / total
            ms["completion_rate"] = completion_rate

            if completion_rate >= 1.0:
                completed_milestones.append(ms)
            else:
                active_milestones.append(ms)

    return {
        "completed_milestones": completed_milestones,
        "active_milestones": active_milestones
    }


def check_project_board() -> Dict[str, Any]:
    """プロジェクトボードの状態を確認"""
    # TODO: GitHub Projects v2 APIを使用してボードの状態を取得
    # 現時点ではプレースホルダー
    return {
        "needs_board_update": True  # 常にボード更新を推奨
    }


def check_stagnant_tasks() -> Dict[str, Any]:
    """停滞タスクを確認"""
    cutoff_date = (datetime.now() - timedelta(hours=48)).isoformat()
    stagnant_drafts = run_command(
        f"gh pr list --state open --draft --json number,title,updatedAt,headRefName | "
        f"jq '[.[] | select(.updatedAt < \"{cutoff_date}\")]'"
    )

    stagnant = json.loads(stagnant_drafts["stdout"]) if stagnant_drafts["success"] else []

    return {
        "stagnant_draft_prs": stagnant
    }


def check_ci_health() -> Dict[str, Any]:
    """CI/CD健全性を確認"""
    recent_runs = run_command("gh run list --limit 10 --json conclusion,status,name")
    runs = json.loads(recent_runs["stdout"]) if recent_runs["success"] else []

    failed_runs = [r for r in runs if r.get("conclusion") == "failure"]

    return {
        "recent_failures": len(failed_runs),
        "has_failures": len(failed_runs) > 0,
        "failed_runs": failed_runs[:3]
    }


def check_documentation() -> Dict[str, Any]:
    """ドキュメント更新が必要か確認"""
    # README.mdとdocsディレクトリの最終更新日時を確認
    readme_check = run_command("git log -1 --format=%ct README.md 2>/dev/null || echo 0")
    code_check = run_command("git log -1 --format=%ct --all -- '*.py' '*.js' '*.ts' '*.tsx' 2>/dev/null || echo 0")

    readme_time = int(readme_check["stdout"]) if readme_check["success"] else 0
    code_time = int(code_check["stdout"]) if code_check["success"] else 0

    # コードの方が新しい場合、ドキュメント更新が必要かも
    needs_doc_update = code_time > readme_time and (code_time - readme_time) > 86400 * 7  # 7日以上

    return {
        "needs_doc_update": needs_doc_update,
        "readme_age_days": (datetime.now().timestamp() - readme_time) / 86400 if readme_time > 0 else 0
    }


def generate_actions(analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """分析結果から実行すべきアクションを生成"""
    actions = []

    # Critical: 初回セットアップ
    if analysis["setup"]["needs_setup"]:
        actions.append({
            "priority": "CRITICAL",
            "action": "initial_setup",
            "description": f"初回セットアップを実行（マイルストーン: {analysis['setup']['milestone_count']}/5, ラベル: {analysis['setup']['label_count']}/4, プロジェクト: {analysis['setup']['has_project']}）",
            "instructions": [
                "1. `cat .github/templates/project-setup.md` を実行してプロジェクト要件を読む",
                "2. 不足しているリソースを作成:",
                "   - GitHubプロジェクト（存在しない場合）",
                "   - マイルストーン（5件必要）",
                "   - 優先度ラベル（priority:critical/high/medium/low）",
                "   - カテゴリラベル（feature/bug/documentation等）",
                "   - 各マイルストーンの初期Issue",
                "3. プロジェクトをリポジトリにリンク",
                "4. 完了報告をこのIssueに投稿"
            ]
        })
        return actions

    draft_issues = set(analysis["prs"]["draft_issues"])

    # Critical: マイルストーン完了時の処理
    if analysis["milestones"]["completed_milestones"]:
        for ms in analysis["milestones"]["completed_milestones"]:
            actions.append({
                "priority": "CRITICAL",
                "action": "close_milestone",
                "milestone_number": ms["number"],
                "description": f"マイルストーン #{ms['number']} \"{ms['title']}\" を完了（100%達成）",
                "instructions": [
                    f"1. マイルストーン完了を確認:",
                    f"   gh api repos/:owner/:repo/milestones/{ms['number']}",
                    f"",
                    f"2. マイルストーンをクローズ:",
                    f"   gh api repos/:owner/:repo/milestones/{ms['number']} -X PATCH -f state=closed",
                    f"",
                    f"3. 完了報告Issueを作成:",
                    f"   gh issue create --title '🎉 マイルストーン {ms['title']} 完了' --body 'マイルストーン {ms['title']} の全タスクが完了しました。\\n\\n次のマイルストーンに進みます。' --label 'documentation,priority:high'",
                    f"",
                    f"4. 次のマイルストーンの準備:",
                    f"   - 次マイルストーンのIssueを確認",
                    f"   - 優先順位を見直し"
                ]
            })

    # Critical: マージ済みPRの事後チェック
    if analysis["merged_prs"]["recent_merged_prs"]:
        for pr in analysis["merged_prs"]["recent_merged_prs"][:2]:
            actions.append({
                "priority": "HIGH",
                "action": "post_merge_check",
                "pr_number": pr["number"],
                "description": f"マージ済みPR #{pr['number']} の事後チェック: {pr['title']}",
                "instructions": [
                    f"1. マージされた変更を確認:",
                    f"   gh pr view {pr['number']} --json files,additions,deletions",
                    f"",
                    f"2. 動作確認が必要な場合:",
                    f"   - developブランチをpull",
                    f"   - ビルド・テストを実行",
                    f"   - 動作確認",
                    f"",
                    f"3. 問題があればBug Issueを作成:",
                    f"   gh issue create --title 'Bug: PR #{pr['number']} のマージ後に発見された問題' --body '...' --label 'bug,priority:high'",
                    f"",
                    f"4. 改善提案があればEnhancement Issueを作成:",
                    f"   gh issue create --title 'Enhancement: PR #{pr['number']} の改善提案' --body '...' --label 'enhancement,priority:medium'"
                ]
            })

    # Critical: バグとCriticalなIssue（Draft PRがないもののみ）
    if analysis["issues"]["critical_issues"]:
        for issue in analysis["issues"]["critical_issues"][:3]:
            issue_num = str(issue['number'])
            if issue_num in draft_issues:
                continue

            actions.append({
                "priority": "CRITICAL",
                "action": "implement_critical_issue",
                "issue_number": issue['number'],
                "description": f"Critical Issue #{issue['number']} を実装: {issue['title']}",
                "instructions": [
                    f"⚠️ 必須: 以下の順序で作業してください:",
                    f"",
                    f"1. ブランチを作成:",
                    f"   git checkout develop",
                    f"   git pull origin develop",
                    f"   git checkout -b feature/issue-{issue['number']}",
                    f"",
                    f"2. 空コミットでDraft PRを先に作成:",
                    f"   git commit --allow-empty -m 'WIP: Issue #{issue['number']} の実装開始'",
                    f"   git push origin feature/issue-{issue['number']}",
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
                    f"   git checkout develop",
                    f"   git pull origin develop",
                    f"   git checkout -b fix/issue-{issue['number']}",
                    f"",
                    f"2. 空コミットでDraft PRを先に作成:",
                    f"   git commit --allow-empty -m 'WIP: Fix #{issue['number']} の修正開始'",
                    f"   git push origin fix/issue-{issue['number']}",
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
                    f"   gh pr ready --undo"
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
                    f"   git pull origin develop",
                    f"",
                    f"4. プロジェクトボードを更新:",
                    f"   該当IssueをDoneに移動（手動またはgh project item-edit）"
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
                    f"   - セキュリティ脆弱性がないか確認",
                    f"",
                    f"3. レビュー結果を投稿:",
                    f"   gh pr review {pr['number']} --approve -b 'LGTM!'",
                    f"   または",
                    f"   gh pr review {pr['number']} --request-changes -b '修正が必要です: ...'",
                    f"   または",
                    f"   gh pr review {pr['number']} --comment -b 'コメント: ...'",
                    f"",
                    f"4. 改善提案があれば別Issueを作成:",
                    f"   gh issue create --title 'Enhancement: PR #{pr['number']} の改善提案' --body '...' --label 'enhancement'"
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

    # Medium: プロジェクトボード更新
    if analysis["board"]["needs_board_update"]:
        actions.append({
            "priority": "MEDIUM",
            "action": "update_project_board",
            "description": "プロジェクトボードを最新状態に更新",
            "instructions": [
                "1. オープンなIssue/PRをボードに追加:",
                "   PROJECT_NUMBER=$(gh project list --owner @me --format json | jq -r '.projects[0].number')",
                "   gh issue list --json number,url | jq -r '.[].url' | while read url; do",
                "     gh project item-add $PROJECT_NUMBER --owner @me --url $url 2>/dev/null || true",
                "   done",
                "",
                "2. PRもボードに追加:",
                "   gh pr list --json number,url | jq -r '.[].url' | while read url; do",
                "     gh project item-add $PROJECT_NUMBER --owner @me --url $url 2>/dev/null || true",
                "   done"
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

    # Medium: ドキュメント更新
    if analysis["docs"]["needs_doc_update"]:
        actions.append({
            "priority": "MEDIUM",
            "action": "update_documentation",
            "description": f"ドキュメント更新（READMEが{analysis['docs']['readme_age_days']:.0f}日更新されていません）",
            "instructions": [
                "1. 最近の変更を確認:",
                "   git log --since='7 days ago' --oneline --all",
                "",
                "2. ドキュメント更新Issueを作成:",
                "   gh issue create --title 'Documentation: README更新' --body '最近のコード変更に合わせてREADMEを更新する必要があります。\\n\\n- 新機能の説明追加\\n- APIドキュメント更新\\n- 使用方法の更新' --label 'documentation,priority:medium'"
            ]
        })

    # Medium: 古いIssueの見直し
    if analysis["issues"]["old_issues"]:
        actions.append({
            "priority": "LOW",
            "action": "review_old_issues",
            "description": f"30日以上経過したIssue {len(analysis['issues']['old_issues'])}件の見直し",
            "instructions": [
                "1. 各Issueの状態を確認:",
            ] + [
                f"   gh issue view {issue['number']}  # {issue['title']}"
                for issue in analysis["issues"]["old_issues"]
            ] + [
                "",
                "2. 以下の判断を実施:",
                "   - まだ有効 → 優先度を更新",
                "   - 不要 → クローズ",
                "   - 分割が必要 → 新しいIssueを作成してクローズ"
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
            ] + [
                f"   gh run view <run-id>  # {run.get('name', 'Unknown')}"
                for run in analysis["ci"]["failed_runs"]
            ] + [
                "",
                "3. 原因を特定して修正:",
                "   - テスト失敗 → テストを修正",
                "   - ビルド失敗 → ビルド設定を修正",
                "   - リンターエラー → コードスタイルを修正",
                "",
                "4. 修正をコミット・プッシュ",
                "",
                "5. 修正が複雑な場合はIssueを作成:",
                "   gh issue create --title 'CI: ビルド失敗の修正' --body '...' --label 'infrastructure,priority:high'"
            ]
        })

    return actions


def main():
    """メイン処理"""
    print("🔍 完全自動化開発サイクル - プロジェクト分析を開始...")
    print()

    # 各項目を分析
    analysis = {
        "setup": check_initial_setup(),
        "prs": check_prs(),
        "merged_prs": check_merged_prs(),
        "issues": check_issues(),
        "milestones": check_milestones(),
        "board": check_project_board(),
        "stagnant": check_stagnant_tasks(),
        "ci": check_ci_health(),
        "docs": check_documentation()
    }

    # アクションを生成
    actions = generate_actions(analysis)

    if not actions:
        print("✅ アクションは必要ありません。プロジェクトは良好な状態です。")
        print()
        print("📊 プロジェクト状態:")
        print(f"  - アクティブマイルストーン: {len(analysis['milestones']['active_milestones'])}件")
        print(f"  - オープンPR: {len(analysis['prs']['needs_review']) + len(analysis['prs']['draft_prs'])}件")
        print(f"  - マージ可能PR: {len(analysis['prs']['ready_to_merge'])}件")
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
    print("- マージ後は必ず事後チェックを実行してください")
    print("- 少なくとも1つのアクションを完了してください")


if __name__ == "__main__":
    main()
