# 项目工时跟踪脚本

一个用于自动统计工程开发时间的Python脚本，可以记录从打开工程到关闭工程的累计工时。

## 功能特性

- ✅ 自动记录工程开发时间
- ✅ 支持累计计时（关闭后不清零，下次打开累加）
- ✅ 按日统计工时
- ✅ 查看实时跟踪状态
- ✅ 生成工时汇总报告
- ✅ 支持重置数据

## 安装要求

- Python 3.6+
- 无需额外安装依赖库

## 使用方法

### 1. 开始工时跟踪

```bash
python project_time_tracker.py start
```

参数：
- `-n, --name`: 项目名称（默认：SLT_GUI）

### 2. 停止工时跟踪

```bash
python project_time_tracker.py stop
```

### 3. 查看当前状态

```bash
python project_time_tracker.py status
```

### 4. 查看工时汇总

```bash
# 查看所有日期的工时记录
python project_time_tracker.py summary

# 查看特定日期的工时记录
python project_time_tracker.py summary -d 2025-12-24
```

参数：
- `-d, --date`: 特定日期，格式：YYYY-MM-DD

### 5. 重置工时数据

```bash
python project_time_tracker.py reset
```

## 示例输出

### 开始跟踪
```
✅ 工时跟踪已开始
  项目: SLT_GUI
  开始时间: 2025-12-24 00:05:30
```

### 查看状态
```
🏗️  项目工时跟踪状态
  项目名称: SLT_GUI
  跟踪状态: 正在运行
  开始时间: 2025-12-24 00:05:30
  当前会话: 0:00:17
  今日累计: 0小时0分钟
  总累计: 0小时0分钟
```

### 停止跟踪
```
✓ 工时跟踪已停止
  项目: SLT_GUI
  开始时间: 2025-12-24 00:05:30
  结束时间: 2025-12-24 00:06:01
  本次会话: 0:00:31
  今日累计: 0小时0分钟
  总累计: 0小时0分钟
```

### 查看汇总
```
📊 项目工时汇总
  项目名称: SLT_GUI
  总累计工时: 2小时30分钟

📅 每日工时记录:
  日期          工时               会话次数
  ------------ --------------- ----------
  2025-12-24   1小时15分钟         2
  2025-12-23   1小时15分钟         3
```

## 数据存储

- 项目数据存储在用户主目录下的 `.slt_gui_project_time.json` 文件中
- 日志记录在当前目录下的 `project_time_tracker.log` 文件中

## 建议使用方式

1. 打开Trae IDE时，运行 `python tools/project_time_tracker.py start` 开始计时
2. 关闭Trae IDE时，运行 `python tools/project_time_tracker.py stop` 停止计时
3. 定期使用 `python tools/project_time_tracker.py status` 查看当前状态
4. 项目结束时，使用 `python tools/project_time_tracker.py summary` 生成工时报告

## 注意事项

- 脚本会自动累计每天的工时
- 如果忘记停止跟踪，下次启动时会继续累计
- 可以随时使用 `status` 命令查看当前跟踪状态
