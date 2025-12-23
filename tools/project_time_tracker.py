#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目工时跟踪脚本
用于统计从打开工程到关闭工程的累计时间
"""

import os
import time
import datetime
import argparse
import logging
import json
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('project_time_tracker.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 项目数据文件路径
PROJECT_DATA_FILE = Path('.') / ".slt_gui_project_time.json"

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='项目工时跟踪脚本')
    parser.add_argument(
        'action',
        choices=['start', 'stop', 'status', 'summary', 'reset'],
        help='要执行的操作: start(开始计时), stop(停止计时), status(查看状态), summary(工时汇总), reset(重置计时)'
    )
    parser.add_argument(
        '-n', '--name',
        type=str,
        default='SLT_GUI',
        help='项目名称（用于数据记录）'
    )
    parser.add_argument(
        '-d', '--date',
        type=str,
        help='查询特定日期的工时，格式：YYYY-MM-DD'
    )
    return parser.parse_args()

def load_project_data():
    """加载项目数据"""
    if PROJECT_DATA_FILE.exists():
        try:
            with open(PROJECT_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"加载项目数据失败: {e}")
            return None
    return None

def save_project_data(data):
    """保存项目数据"""
    try:
        with open(PROJECT_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        logger.error(f"保存项目数据失败: {e}")
        return False

def get_today_date_str():
    """获取今天的日期字符串，格式：YYYY-MM-DD"""
    return datetime.datetime.now().strftime('%Y-%m-%d')

def start_tracking(project_name):
    """开始工时跟踪"""
    project_data = load_project_data()
    today_date = get_today_date_str()
    
    if not project_data:
        # 创建新的项目数据结构
        project_data = {
            'project_name': project_name,
            'total_hours': 0,
            'total_minutes': 0,
            'is_running': True,
            'start_time': time.time(),
            'start_datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'daily_records': {
                today_date: {
                    'date': today_date,
                    'hours': 0,
                    'minutes': 0,
                    'sessions': []
                }
            }
        }
    else:
        if project_data.get('is_running', False):
            logger.warning(f"工时跟踪已在运行中，开始时间: {project_data['start_datetime']}")
            print(f"⚠️  工时跟踪已在运行中")
            print(f"  开始时间: {project_data['start_datetime']}")
            return False
        
        # 确保今天的记录存在
        if today_date not in project_data['daily_records']:
            project_data['daily_records'][today_date] = {
                'date': today_date,
                'hours': 0,
                'minutes': 0,
                'sessions': []
            }
        
        # 更新项目数据
        project_data['is_running'] = True
        project_data['start_time'] = time.time()
        project_data['start_datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if save_project_data(project_data):
        logger.info(f"=== 项目 '{project_name}' 工时跟踪开始于 {project_data['start_datetime']} ===")
        print(f"✓ 工时跟踪已开始")
        print(f"  项目: {project_name}")
        print(f"  开始时间: {project_data['start_datetime']}")
        return True
    else:
        return False

def stop_tracking():
    """停止工时跟踪"""
    project_data = load_project_data()
    
    if not project_data or not project_data.get('is_running', False):
        logger.warning("没有正在运行的工时跟踪")
        print("⚠️  没有正在运行的工时跟踪")
        return False
    
    # 记录结束时间
    end_time = time.time()
    end_datetime = datetime.datetime.now()
    today_date = end_datetime.strftime('%Y-%m-%d')
    
    # 计算本次会话持续时间
    start_timestamp = project_data['start_time']
    session_duration = end_time - start_timestamp
    session_duration_str = str(datetime.timedelta(seconds=round(session_duration)))
    
    # 转换为小时和分钟
    session_hours = int(session_duration // 3600)
    session_minutes = int((session_duration % 3600) // 60)
    
    # 更新今日记录
    today_record = project_data['daily_records'][today_date]
    today_record['hours'] += session_hours
    today_record['minutes'] += session_minutes
    
    # 处理分钟进位
    if today_record['minutes'] >= 60:
        today_record['hours'] += today_record['minutes'] // 60
        today_record['minutes'] = today_record['minutes'] % 60
    
    # 添加会话记录
    today_record['sessions'].append({
        'start_time': project_data['start_datetime'],
        'end_time': end_datetime.strftime('%Y-%m-%d %H:%M:%S'),
        'duration': session_duration_str,
        'hours': session_hours,
        'minutes': session_minutes
    })
    
    # 更新总工时
    project_data['total_hours'] += session_hours
    project_data['total_minutes'] += session_minutes
    
    # 处理总分钟进位
    if project_data['total_minutes'] >= 60:
        project_data['total_hours'] += project_data['total_minutes'] // 60
        project_data['total_minutes'] = project_data['total_minutes'] % 60
    
    # 更新项目数据状态
    project_data['is_running'] = False
    project_data['end_time'] = end_datetime.strftime('%Y-%m-%d %H:%M:%S')
    project_data['last_session_duration'] = session_duration_str
    
    if save_project_data(project_data):
        logger.info(f"=== 项目 '{project_data['project_name']}' 工时跟踪结束于 {end_datetime.strftime('%Y-%m-%d %H:%M:%S')} ===")
        logger.info(f"本次会话持续时间: {session_duration_str}")
        
        print(f"\n✓ 工时跟踪已停止")
        print(f"  项目: {project_data['project_name']}")
        print(f"  开始时间: {project_data['start_datetime']}")
        print(f"  结束时间: {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  本次会话: {session_duration_str}")
        print(f"  今日累计: {today_record['hours']}小时{today_record['minutes']}分钟")
        print(f"  总累计: {project_data['total_hours']}小时{project_data['total_minutes']}分钟")
        
        return True
    else:
        return False

def show_status():
    """显示当前状态"""
    project_data = load_project_data()
    
    if not project_data:
        logger.info("没有项目数据")
        print("⚠️  没有项目数据，请先运行 start 命令开始跟踪")
        return False
    
    today_date = get_today_date_str()
    today_record = project_data['daily_records'].get(today_date, {
        'hours': 0,
        'minutes': 0
    })
    
    print(f"\n🏗️  项目工时跟踪状态")
    print(f"  项目名称: {project_data['project_name']}")
    
    if project_data.get('is_running', False):
        # 计算当前已运行时间
        current_time = time.time()
        current_duration = current_time - project_data['start_time']
        current_duration_str = str(datetime.timedelta(seconds=round(current_duration)))
        
        print(f"  跟踪状态: 正在运行")
        print(f"  开始时间: {project_data['start_datetime']}")
        print(f"  当前会话: {current_duration_str}")
    else:
        print(f"  跟踪状态: 已停止")
        if 'last_session_duration' in project_data:
            print(f"  上次会话: {project_data['last_session_duration']}")
    
    print(f"  今日累计: {today_record['hours']}小时{today_record['minutes']}分钟")
    print(f"  总累计: {project_data['total_hours']}小时{project_data['total_minutes']}分钟")
    
    logger.info(f"项目 '{project_data['project_name']}' 状态查询完成")
    return True

def show_summary(args):
    """显示工时汇总"""
    project_data = load_project_data()
    
    if not project_data:
        logger.info("没有项目数据")
        print("⚠️  没有项目数据")
        return False
    
    print(f"\n📊 项目工时汇总")
    print(f"  项目名称: {project_data['project_name']}")
    print(f"  总累计工时: {project_data['total_hours']}小时{project_data['total_minutes']}分钟")
    
    if args.date:
        # 显示特定日期的工时
        if args.date in project_data['daily_records']:
            record = project_data['daily_records'][args.date]
            print(f"\n📅 日期: {args.date}")
            print(f"  当日工时: {record['hours']}小时{record['minutes']}分钟")
            print(f"  会话次数: {len(record['sessions'])}")
            
            if record['sessions']:
                print(f"  会话记录:")
                for i, session in enumerate(record['sessions'], 1):
                    print(f"    {i}. {session['start_time']} - {session['end_time']} ({session['duration']})")
        else:
            print(f"\n⚠️  没有 {args.date} 的工时记录")
    else:
        # 显示所有日期的工时
        print(f"\n📅 每日工时记录:")
        print(f"  {'日期':<12} {'工时':<15} {'会话次数':<10}")
        print(f"  {'-'*12} {'-'*15} {'-'*10}")
        
        # 按日期排序
        sorted_dates = sorted(project_data['daily_records'].keys(), reverse=True)
        
        for date in sorted_dates:
            record = project_data['daily_records'][date]
            hours_str = f"{record['hours']}小时{record['minutes']}分钟"
            print(f"  {date:<12} {hours_str:<15} {len(record['sessions']):<10}")
    
    logger.info(f"项目 '{project_data['project_name']}' 工时汇总查询完成")
    return True

def reset_tracking():
    """重置工时跟踪数据"""
    if PROJECT_DATA_FILE.exists():
        try:
            PROJECT_DATA_FILE.unlink()
            logger.info("工时跟踪数据已重置")
            print("✓ 工时跟踪数据已重置")
            return True
        except IOError as e:
            logger.error(f"重置工时跟踪数据失败: {e}")
            print(f"⚠️  重置工时跟踪数据失败: {e}")
            return False
    else:
        logger.info("没有工时跟踪数据需要重置")
        print("⚠️  没有工时跟踪数据需要重置")
        return False

def main():
    """主函数"""
    args = parse_arguments()
    
    if args.action == 'start':
        start_tracking(args.name)
    elif args.action == 'stop':
        stop_tracking()
    elif args.action == 'status':
        show_status()
    elif args.action == 'summary':
        show_summary(args)
    elif args.action == 'reset':
        reset_tracking()
    else:
        logger.error(f"未知操作: {args.action}")

if __name__ == '__main__':
    main()
