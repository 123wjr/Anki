from bs4 import BeautifulSoup, Tag

def convert_mathml_to_latex(math_tag):
    def process_element(element):
        if isinstance(element, Tag):
            tag_name = element.name
            children = list(element.children)
            if tag_name == 'mfrac':
                if len(children) >= 2:
                    numerator = process_element(children[0])
                    denominator = process_element(children[1])
                    return f'\\frac{{{numerator}}}{{{denominator}}}'
                return ''
            elif tag_name in ['mn', 'mi', 'mo']:
                return element.get_text(strip=True)
            elif tag_name == 'msup':
                base = process_element(children[0]) if children else ''
                exp = process_element(children[1]) if len(children) > 1 else ''
                return f'{{{base}}}^{{{exp}}}'
            elif tag_name == 'msub':
                base = process_element(children[0]) if children else ''
                sub = process_element(children[1]) if len(children) > 1 else ''
                return f'{{{base}}}_{{{sub}}}'
            elif tag_name == 'mrow':
                return ''.join(process_element(child) for child in children)
            elif tag_name == 'msqrt':
                content = ''.join(process_element(child) for child in children)
                return f'\\sqrt{{{content}}}'
            elif tag_name == 'mroot':
                if len(children) >= 2:
                    base = process_element(children[0])
                    root = process_element(children[1])
                    return f'\\sqrt[{root}]{{{base}}}'
                return ''
            else:
                return ''.join(process_element(child) for child in children)
        else:
            return element.strip() if isinstance(element, str) else ''
    
    latex = ''.join(process_element(child) for child in math_tag.children 
                    if not isinstance(child, str) or child.strip())
    return latex.strip()

def html_to_md(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Process math tags and create placeholders
    math_placeholders = []
    for i, math_tag in enumerate(soup.find_all('math')):
        latex = convert_mathml_to_latex(math_tag)
        placeholder = f'@@MATH_PH_{i}@@'
        math_placeholders.append(f' ${latex}$ ')
        math_tag.replace_with(placeholder)
    
    # Convert to text while preserving whitespace
    text = soup.get_text(strip=False)
    
    # Restore math placeholders
    for i, ph in enumerate(math_placeholders):
        text = text.replace(f'@@MATH_PH_{i}@@', ph)
    
    # Clean up multiple newlines
    text = '\n'.join(line.strip() for line in text.split('\n'))
    return text

if __name__ == '__main__':
    with open('D:/笔记本/课内学习/02数学/测试与预输出/题目.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    md = html_to_md(html)
    
    with open('D:/笔记本/课内学习/02数学/测试与预输出/题目.md', 'w', encoding='utf-8') as f:
        f.write(md)