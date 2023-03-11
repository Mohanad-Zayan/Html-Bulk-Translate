
import os
import mtranslate
from bs4 import BeautifulSoup


#first Approach 
def Transltor(folder): 
    for top,top_down,inside in os.walk(folder):
        os.chdir(top)
        for file in inside:
            if file.endswith("html"):
                print(file)
                with open(file, "r", encoding="utf-8") as f:
                    html = f.read()
                    soup = BeautifulSoup(html, "html.parser")
                    tags = soup.find_all(
                        ['h1', 'h2', 'h3', 'h4', 'p', "a", "svg", "span", "strong", "button", 'title'])
                    for tag in tags:
                        text = tag.get_text()
                        if tag.string is not None:
                            translated_text = mtranslate.translate(text, "hi") #Write target language.
                            print(f"{text} , {translated_text}")
                            tag.string.replace_with(translated_text)

                    # Write the translated HTML to a new file or you can use the same file.
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(str(soup))

Transltor('put/your/directory/here')
#-------------------------------------------------------------------------------
# second approach
folder = 'put/your/directory/here'
for top, top_down, inside in os.walk(folder):
    os.chdir(top)
    for file in inside:
        if file.endswith("html"):
            print(file)
            with open(file, "r", encoding="utf-8") as f:
                html = f.read()
                soup = BeautifulSoup(html, 'lxml')
                tag1 = soup.new_tag("script")
                tag2 = soup.new_tag("script")
                tag2['src'] = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit'
                tag2['type'] = 'text/javascript'
                jscodestring = '''        
                                    function googleTranslateElementInit() {
                                        setCookie('googtrans', '/en/hi', 1);
                                        new google.translate.TranslateElement({ pageLanguage: 'en'});
                                    }
                                    function setCookie(key, value, expiry) {
                                        var expires = new Date();
                                        expires.setTime(expires.getTime() + (expiry * 24 * 60 * 60 * 1000));
                                        document.cookie = key + '=' + value + ';expires=' + expires.toUTCString();
                                    }
                            '''
                tag1.append(jscodestring)
                head = soup.find('head')
                if head is None : continue
                head.append(tag1)
                head.append(tag2)
                print(soup)
                with open(file, "w", encoding="utf8") as f:
                    f.write(str(soup))
