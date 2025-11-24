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
    milestones = run_command("gh api repos/:owner/:repo/milestones | jq 'length'")
    labels = run_command("gh label list | grep -c 'priority:' || true")

    milestone_count = int(milestones["stdout"]) if milestones["success"] else 0
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
    open_prs = run_command("gh pr list --state open --json number,title,isDraft,reviewDecision,statusCheckRollup")
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

    for pr in prs:
        if pr.get("isDraft"):
            draft_prs.append(pr)
        elif pr.get("reviewDecision") == "APPROVED" and pr.get("statusCheckRollup", {}).get("state") == "SUCCESS":
            ready_to_merge.append(pr)
        else:
            needs_review.append(pr)

    return {
        "branches_without_pr": branches_without_pr,
        "ready_to_merge": ready_to_merge,
        "needs_review": needs_review,
        "draft_prs": draft_prs
    }


def check_issues() -> Dict[str, Any]:
    """Issue優先順位を確認"""
    critical = run_command("gh issue list --label 'priority:critical' --json number,title")
    bugs = run_command("gh issue list --label 'bug' --json number,title")

    critical_issues = json.loads(critical["stdout"]) if critical["success"] else []
    bug_issues = json.loads(bugs["stdout"]) if bugs["success"] else []

    return {
        "critical_issues": critical_issues,
        "bug_issues": bug_issues
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


def generate_actions(analysis: Dict[str, Any]) -> List[Dict[str, str]]:
    """分析結果から実行すべきアクションを生成"""
    actions = []

    # Critical: 初回セットアップ
    if analysis["setup"]["needs_setup"]:
        actions.append({
            "priority": "CRITICAL",
            "action": "initial_setup",
            "description": f"初回セットアップを実行（マイルストーン: {analysis['setup']['milestone_count']}/5, ラベル: {analysis['setup']['label_count']}/4）",
            "command": "cat .github/templates/project-setup.md を読んで、必要なリソースを作成"
        })
        return actions  # セットアップが必要な場合は他の処理をスキップ

    # Critical: バグとCriticalなIssue
    if analysis["issues"]["critical_issues"]:
        for issue in analysis["issues"]["critical_issues"][:3]:  # 最大3件
            actions.append({
                "priority": "CRITICAL",
                "action": "implement_issue",
                "description": f"Critical Issue #{issue['number']} を実装: {issue['title']}",
                "command": f"gh issue comment {issue['number']} --body '@claude このIssueを実装してください'"
            })

    if analysis["issues"]["bug_issues"]:
        for issue in analysis["issues"]["bug_issues"][:2]:  # 最大2件
            actions.append({
                "priority": "CRITICAL",
                "action": "fix_bug",
                "description": f"Bug #{issue['number']} を修正: {issue['title']}",
                "command": f"gh issue comment {issue['number']} --body '@claude このバグを修正してください'"
            })

    # High: PR未作成のブランチ
    if analysis["prs"]["branches_without_pr"]:
        for branch in analysis["prs"]["branches_without_pr"][:3]:  # 最大3件
            actions.append({
                "priority": "HIGH",
                "action": "create_pr",
                "description": f"ブランチ {branch} のPRを作成",
                "command": f"gh pr create --head {branch} --title 'PR for {branch}' --body 'Auto-created PR' --base develop"
            })

    # High: マージ可能なPR
    if analysis["prs"]["ready_to_merge"]:
        for pr in analysis["prs"]["ready_to_merge"][:3]:  # 最大3件
            actions.append({
                "priority": "HIGH",
                "action": "merge_pr",
                "description": f"PR #{pr['number']} をマージ: {pr['title']}",
                "command": f"gh pr merge {pr['number']} --squash --delete-branch"
            })

    # High: レビュー待ちPR
    if analysis["prs"]["needs_review"]:
        for pr in analysis["prs"]["needs_review"][:2]:  # 最大2件
            actions.append({
                "priority": "HIGH",
                "action": "review_pr",
                "description": f"PR #{pr['number']} をレビュー: {pr['title']}",
                "command": f"gh pr view {pr['number']} --comments && gh pr review {pr['number']}"
            })

    # High: 停滞タスク
    if analysis["stagnant"]["stagnant_draft_prs"]:
        for pr in analysis["stagnant"]["stagnant_draft_prs"][:2]:  # 最大2件
            actions.append({
                "priority": "HIGH",
                "action": "revive_stagnant",
                "description": f"停滞中のDraft PR #{pr['number']} を再開",
                "command": f"gh pr comment {pr['number']} --body '@claude このPRが停滞しています。実装を継続してください'"
            })

    # Medium: CI失敗
    if analysis["ci"]["has_failures"]:
        actions.append({
            "priority": "MEDIUM",
            "action": "fix_ci",
            "description": f"CI失敗を修正（直近10件中{analysis['ci']['recent_failures']}件失敗）",
            "command": "gh run list --limit 10 で詳細を確認して修正"
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

    print("📋 実行すべきアクション:\n")

    for i, action in enumerate(actions, 1):
        print(f"{i}. [{action['priority']}] {action['description']}")
        print(f"   実行: {action['command']}")
        print()

    # JSON出力（機械可読用）
    print("\n---JSON---")
    print(json.dumps(actions, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
