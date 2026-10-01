import sys
import re

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'function openOnboardingFlow[\s\S]*?(?=function [a-zA-Z0-9_]+\s*\(|$)', text)
if match:
    sys.stdout.reconfigure(encoding='utf-8')
    print('Found openOnboardingFlow function:')
    print(match.group(0)[:4000])

match2 = re.search(r'function renderOnboardingStep[\s\S]*?(?=function [a-zA-Z0-9_]+\s*\(|$)', text)
if match2:
    print('Found renderOnboardingStep function:')
    print(match2.group(0)[:4000])
