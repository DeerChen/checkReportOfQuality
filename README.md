# 批量生成质检报告

## 使用步骤

1. 填写`template/`中的`SN.xlsx`，对应型号和序列号
2. 运行软件，依需选择模板文件路径
3. 在`result/`中查看批量生成的产品质检报告

## 生成exe

```python
pyinstaller.exe -F -w -i .\assets\ico\sn.ico -n 批量生成质检报告 --key checkReportOfQuality --clean --win-private-assemblies .\main.py
# 将assets封装进data
pyinstaller.exe -F .\批量生成质检报告.spec
```