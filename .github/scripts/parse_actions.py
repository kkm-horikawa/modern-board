#!/usr/bin/env python3
"""
コメント内容を解析して実行可能なアクションを抽出する

Usage:
    python3 parse_actions.py <comment_body>
"""

import sys
import json
import re
from typing import List, Dict, Any


def parse_action_items(comment_body: str) -> List[Dict[str, Any]]:
    """
    コメント本文から実行可能なアクションを抽出する

    Args:
        comment_body: コメント本文

    Returns:
        アクション項目のリスト
    """
    actions = []

    # アクションセクションを探す
    action_patterns = [
        r'##?\s*(?:実行可能な)?アクション(?:項目)?[:：]?\s*\n(.*?)(?=\n##|\Z)',
        r'##?\s*(?:推奨|提案)アクション[:：]?\s*\n(.*?)(?=\n##|\Z)',
        r'##?\s*次のステップ[:：]?\s*\n(.*?)(?=\n##|\Z)',
        r'##?\s*TODO[:：]?\s*\n(.*?)(?=\n##|\Z)',
    ]

    action_text = ""
    for pattern in action_patterns:
        match = re.search(pattern, comment_body, re.DOTALL | re.MULTILINE | re.IGNORECASE)
        if match:
            action_text = match.group(1)
            break

    if not action_text:
        # フォールバック: コメント全体を検索
        action_text = comment_body

    # 各種アクションキーワードを検索
    action_keywords = {
        'create_issue': [
            r'(?:Issue|issue|イシュー).*?(?:作成|発行)',
            r'(?:作成|発行).*?(?:Issue|issue|イシュー)',
            r'新規.*?(?:Issue|issue|イシュー)',
        ],
        'update_labels': [
            r'(?:ラベル|label).*?(?:更新|変更|追加|削除)',
            r'(?:更新|変更|追加|削除).*?(?:ラベル|label)',
        ],
        'update_priority': [
            r'(?:優先度|priority).*?(?:更新|変更|見直し)',
            r'(?:更新|変更|見直し).*?(?:優先度|priority)',
        ],
        'merge_pr': [
            r'PR.*?(?:マージ|merge)',
            r'(?:マージ|merge).*?PR',
            r'プルリクエスト.*?(?:マージ|merge)',
        ],
        'create_pr': [
            r'PR.*?(?:作成|create)',
            r'(?:作成|create).*?PR',
            r'プルリクエスト.*?(?:作成|オープン)',
        ],
        'close_issue': [
            r'(?:Issue|issue|イシュー).*?(?:クローズ|閉じる|close)',
            r'(?:クローズ|閉じる|close).*?(?:Issue|issue|イシュー)',
        ],
        'review_pr': [
            r'PR.*?(?:レビュー|review)',
            r'(?:レビュー|review).*?PR',
        ],
        'update_milestone': [
            r'(?:マイルストーン|milestone).*?(?:更新|変更)',
            r'(?:更新|変更).*?(?:マイルストーン|milestone)',
        ],
        'close_milestone': [
            r'(?:マイルストーン|milestone).*?(?:クローズ|完了|close)',
            r'(?:クローズ|完了|close).*?(?:マイルストーン|milestone)',
        ],
    }

    # 各行を解析
    lines = action_text.split('\n')
    current_action = None

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # リスト項目かチェック
        is_list_item = line.startswith(('-', '*', '•', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.'))

        if is_list_item:
            # リスト項目からマーカーを削除
            line_content = re.sub(r'^[-*•]|\d+\.', '', line).strip()

            # アクションタイプを判定
            action_type = None
            for atype, patterns in action_keywords.items():
                for pattern in patterns:
                    if re.search(pattern, line_content, re.IGNORECASE):
                        action_type = atype
                        break
                if action_type:
                    break

            if action_type:
                # Issue番号やPR番号を抽出
                issue_numbers = re.findall(r'#(\d+)', line_content)

                action = {
                    'type': action_type,
                    'description': line_content,
                    'issue_numbers': issue_numbers,
                    'priority': extract_priority(line_content),
                }

                actions.append(action)
                current_action = action
        else:
            # リスト項目でない場合は、前のアクションの詳細情報として追加
            if current_action and line:
                if 'details' not in current_action:
                    current_action['details'] = []
                current_action['details'].append(line)

    return actions


def extract_priority(text: str) -> str:
    """
    テキストから優先度を抽出
    """
    text_lower = text.lower()

    if any(word in text_lower for word in ['critical', 'クリティカル', '緊急', '最優先']):
        return 'critical'
    elif any(word in text_lower for word in ['high', '高', '重要']):
        return 'high'
    elif any(word in text_lower for word in ['medium', '中', '通常']):
        return 'medium'
    elif any(word in text_lower for word in ['low', '低', '低優先度']):
        return 'low'

    return 'medium'


def generate_claude_instructions(actions: List[Dict[str, Any]], issue_number: str) -> str:
    """
    抽出したアクションからClaude向けの指示文を生成

    Args:
        actions: アクション項目のリスト
        issue_number: 元のIssue番号

    Returns:
        Claude向けの指示文
    """
    if not actions:
        return ""

    # 優先度でソート
    priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    actions.sort(key=lambda x: priority_order.get(x.get('priority', 'medium'), 2))

    instructions = f"@claude\n\nIssue #{issue_number} の分析結果に基づいて、以下のアクションを実行してください：\n\n"

    action_descriptions = {
        'create_issue': 'Issue作成',
        'update_labels': 'ラベル更新',
        'update_priority': '優先度変更',
        'merge_pr': 'PRマージ',
        'create_pr': 'PR作成',
        'close_issue': 'Issueクローズ',
        'review_pr': 'PRレビュー',
        'update_milestone': 'マイルストーン更新',
        'close_milestone': 'マイルストーン完了',
    }

    for i, action in enumerate(actions, 1):
        action_type = action['type']
        description = action['description']
        priority = action.get('priority', 'medium')

        priority_emoji = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢',
        }.get(priority, '🟡')

        instructions += f"{i}. {priority_emoji} **{action_descriptions.get(action_type, action_type)}**: {description}\n"

        if action.get('details'):
            for detail in action['details']:
                instructions += f"   - {detail}\n"

        instructions += "\n"

    instructions += "\n---\n\n"
    instructions += "**注意事項:**\n"
    instructions += "- 各アクションを実行する前に、現在の状態を確認してください\n"
    instructions += "- Issue番号やPR番号が指定されている場合は、それを使用してください\n"
    instructions += "- エラーが発生した場合は、元のIssueにコメントで報告してください\n"
    instructions += f"- 完了後、Issue #{issue_number} にサマリーを投稿してください\n"

    return instructions


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            'error': 'Usage: python3 parse_actions.py <comment_body>',
            'actions': [],
            'instructions': ''
        }))
        sys.exit(1)

    comment_body = sys.argv[1]

    # アクションを抽出
    actions = parse_action_items(comment_body)

    # Issue番号を抽出（環境変数から取得する想定）
    import os
    issue_number = os.environ.get('ISSUE_NUMBER', 'unknown')

    # Claude向けの指示文を生成
    instructions = ""
    if actions:
        instructions = generate_claude_instructions(actions, issue_number)

    # 結果を出力
    result = {
        'actions': actions,
        'instructions': instructions,
        'has_actions': len(actions) > 0
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
