import re

def layout_md0(text, max_width=50):
    """
    Lays out md0 text with word wrapping at max_width characters.

    Returns:
        (laid_out_text, links)
        - laid_out_text: string with text laid out at most max_width chars per line
        - links: dict where links[i] = {url: str, refs: [(text, position), ...]}
    """
    output_lines = []
    links = {}

    current_line = ""
    x = 0
    y = 0

    for line in text.split('\n'):
        link_def_match = re.match(r'^\[(\d+)\]:\s(\S+)$', line)
        if link_def_match:
            id = int(link_def_match.group(1))
            url = link_def_match.group(2)
            if id not in links:
                links[id] = {'url': url, 'refs': []}
            else:
                links[id]['url'] = url
        else:
            image_match = re.match(r'^\!\[([^\[\]]+)\]\[(\d+)\]$', line)
            if image_match:
                alt_text = image_match.group(1)
                id = int(image_match.group(2))
                rendered_image = f"![img]: {alt_text}"

                if id not in links:
                    links[id] = {'url': None, 'refs': []}
                links[id]['refs'].append((rendered_image, (y, x)))

                output_lines.append(rendered_image)
                y += 1
            else:
                for token in line.split():
                    link_match = re.match(r'^\[(\S+)\]\[(\d+)\](\S*)$', token)

                    if link_match:
                        linktext = link_match.group(1)
                        id = int(link_match.group(2))
                        trailing = link_match.group(3)

                        rendered_link = f"[{linktext}]"
                        if x + len(rendered_link) > max_width:
                            output_lines.append(current_line.rstrip())
                            current_line = ""
                            x = 0
                            y += 1

                        if id not in links:
                            links[id] = {'url': None, 'refs': []}
                        links[id]['refs'].append((rendered_link, (y, x)))

                        current_line += rendered_link
                        x += len(rendered_link)

                        if trailing:
                            if x + len(trailing) > max_width:
                                output_lines.append(current_line.rstrip())
                                current_line = ""
                                x = 0
                                y += 1

                            current_line += trailing
                            x += len(trailing)

                        if x + 1 <= max_width:
                            current_line += " "
                            x += 1
                    else: # plain text
                        if x + len(token) > max_width:
                            output_lines.append(current_line.rstrip())
                            current_line = ""
                            x = 0
                            y += 1

                        current_line += token
                        x += len(token)

                        if x + 1 <= max_width:
                            current_line += " "
                            x += 1

                output_lines.append(current_line.rstrip())
                current_line = ""
                x = 0
                y += 1

    laid_out_text = '\n'.join(output_lines)
    return laid_out_text, links

def test_layout():
    with open('README.md', 'r') as f:
        test_input = f.read()

    laid_out, links = layout_md0(test_input)

    with open('expected_output.txt', 'r') as f:
        expected_output = f.read()

    expected_links = {
        1: {'url': 'https://commonmark.org', 'refs': [('[markdown]', (2, 17))]},
        2: {'url': 'https://geminiprotocol.net/docs/gemtext-specification.gmi', 'refs': [('[gemtext]', (13, 25)), ('[link]', (28, 17))]},
        3: {'url': 'https://github.com/remysucre/md0', 'refs': [('[`render.py`]', (59, 13))]},
        4: {'url': 'https://play.date', 'refs': [('[Playdate]', (8, 39))]},
        5: {'url': 'demo.gif', 'refs': [('![img]: md0 on Playdate', (11, 0))]},
        6: {'url': 'https://github.com/remysucre/ORBIT', 'refs': [('[ORBIT]', (8, 16))]}
    }

    assert laid_out == expected_output, f"Layout output mismatch"
    assert links == expected_links, f"Links mismatch"

if __name__ == "__main__":
    test_layout()
