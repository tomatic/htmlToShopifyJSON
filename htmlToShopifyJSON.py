from bs4 import BeautifulSoup
import json

def html_to_json(html):
    soup = BeautifulSoup(html, "html.parser")
    
    def parse_element(element):
        if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            return {
                "type": "heading",
                "children": [{"type": "text", "value": element.get_text(strip=True)}],
                "level": int(element.name[1])
            }
        
        elif element.name == "p":
            children = []
            for child in element.children:
                if child.name == "em":
                    children.append({"type": "text", "value": child.get_text(strip=True), "italic": True})
                elif child.name == "strong":
                    children.append({"type": "text", "value": child.get_text(strip=True), "bold": True})
                elif child.name == "a":
                    if child.has_attr("target"):
                        if child.has_attr("title"):
                            children.append({"type": "link", "url": child["href"], "target": child["target"], "title": child["title"], "children": [{"type": "text", "value": child.get_text(strip=True)}]})
                        else:
                            children.append({"type": "link", "url": child["href"], "children": [{"type": "text", "value": child.get_text(strip=True)}]})
                    else:
                        if child.has_attr("title"):
                            children.append({"type": "link", "url": child["href"], "title": child["title"], "children": [{"type": "text", "value": child.get_text(strip=True)}]})
                        else:
                          children.append({"type": "link", "url": child["href"], "children": [{"type": "text", "value": child.get_text(strip=True)}]})
                elif child.name is None:
                    children.append({"type": "text", "value": child.strip()})
            return {"type": "paragraph", "children": children}
        
        elif element.name in ["ul", "ol"]:
            list_type = "unordered" if element.name == "ul" else "ordered"
            children = []
            for li in element.find_all("li", recursive=False):
                children.append(parse_element(li))
            return {"listType": list_type, "type": "list", "children": children}
        
        elif element.name == "li":
            children = []
            for child in element.children:
                if child.name == "i":
                    children.append({"type": "text", "value": child.get_text(strip=True), "italic": True})
                elif child.name == "strong":
                    children.append({"type": "text", "value": child.get_text(strip=True), "bold": True})
                elif child.name is None:
                    children.append({"type": "text", "value": child.strip()})
            return {"type": "list-item", "children": children}
        
        return None

    root = {"type": "root", "children": []}
    for element in soup.children:
        parsed_element = parse_element(element)
        if parsed_element:
            root["children"].append(parsed_element)
    
    return json.dumps(root, indent=2)

# Read contents of test.html into a string
with open("test.html") as file:
    html_input = file.read()

print(html_to_json(html_input))
