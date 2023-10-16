import random
import ipaddress
import re
import urllib.request
from bs4 import BeautifulSoup
import socket
import requests
from googlesearch import search
import whois
from datetime import date, datetime
import time
from urllib.parse import urlparse
import os
import random
import urllib
import csv
import socket
import sys

from patterns import *

ipv4_pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
ipv6_pattern = r"^(?:(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){6})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):" \
               r"(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}" \
               r"(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:::(?:(?:(?:[0-9a-fA-F]{1,4})):){5})" \
               r"(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|" \
               r"(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|" \
               r"(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})))?::(?:(?:(?:[0-9a-fA-F]{1,4})):){4})" \
               r"(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|" \
               r"(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|" \
               r"(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,1}(?:(?:[0-9a-fA-F]{1,4})))?::" \
               r"(?:(?:(?:[0-9a-fA-F]{1,4})):){3})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|" \
               r"(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}" \
               r"(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,2}" \
               r"(?:(?:[0-9a-fA-F]{1,4})))?::(?:(?:(?:[0-9a-fA-F]{1,4})):){2})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):" \
               r"(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|" \
               r"(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,3}" \
               r"(?:(?:[0-9a-fA-F]{1,4})))?::(?:(?:[0-9a-fA-F]{1,4})):)(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):" \
               r"(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}" \
               r"(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,4}" \
               r"(?:(?:[0-9a-fA-F]{1,4})))?::)(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|" \
               r"(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|" \
               r"(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,5}" \
               r"(?:(?:[0-9a-fA-F]{1,4})))?::)(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,6}" \
               r"(?:(?:[0-9a-fA-F]{1,4})))?::))))$"
http_https = r"https://|http://"

'''
1 is legitimate
0 suspicious
-1 is phishing
'''

write_file = "Path to saved phishing web pages"
phishing_features_file_path = "Path to CSV file to write phishing features"
phishing_urls_file = "Path to file containing phishing URLs"


def having_ip_address(url):
    try:
        ipaddress.ip_address(url)
        return -1
    except:
        return 1


def url_length(url):
    if len(url) < 54:
        return 1
    elif 54 <= len(url) <= 75:
        return 0
    return -1


def tiny_URL(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',
                      url)
    return -1 if match else 1


def having_at_symbol(url):
    if re.findall("@", url):
        return -1
    else:
        return 1


def double_slash_redirecting(url):
    list_slash = [x.start(0) for x in re.finditer('//', url)]
    return -1 if list_slash[len(list_slash) - 1] > 6 else 1


def prefix_suffix(url):
    return -1 if re.findall(r"https?://[^\-]+-[^\-]+/", url) else 1


def having_sub_domain(url):
    if len(re.findall("\.", url)) == 1:
        return 1
    elif len(re.findall("\.", url)) == 2:
        return 0
    else:
        return -1


# SSLfinal_state
def SSL_final_state(url):
    return 1 if requests.get(url).text else -1


# Domain_registration_length
def Domain_registration_length(url):
    w = whois.whois(url)
    expiration_date = w.expiration_date
    try:
        registration_length = 0
        expiration_date = min(expiration_date)
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        registration_length = abs((expiration_date - today).days)

        if registration_length / 365 <= 1:
            return -1
        else:
            return 1
    except:
        return -1


# Favicon
def favicon(soup, url, domain):
    if soup == -999:
        return -1
    else:
        for head in soup.find_all('head'):
            for head.link in soup.find_all('link', href=True):
                dots = [x.start(0)
                        for x in re.finditer('\.', head.link['href'])]
                if url in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
                    return 1
                else:
                    return -1


# port
def port(domain):
    try:
        port = domain.split(":")[1]
        if port:
            return -1
        else:
            return 1
    except:
        return 1


def https_token(url):
    return 1 if re.findall(r"^https://", url) else -1


# request URL
def request_URL(soup, url, domain):
    i = 0
    success = 0
    for img in soup.find_all('img', src=True):
        dots = [x.start(0) for x in re.finditer('\.', img['src'])]
        if url in img['src'] or domain in img['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for audio in soup.find_all('audio', src=True):
        dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
        if url in audio['src'] or domain in audio['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for embed in soup.find_all('embed', src=True):
        dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
        if url in embed['src'] or domain in embed['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for iframe in soup.find_all('iframe', src=True):
        dots = [x.start(0) for x in re.finditer('\.', iframe['src'])]
        if url in iframe['src'] or domain in iframe['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    try:
        percentage = success / float(i) * 100
        if percentage < 22.0:
            return 1
        elif (percentage >= 22.0) and (percentage < 61.0):
            return 0
        else:
            return -1
    except:
        return 1


# URL_of_Anchor
def URL_of_Anchor(soup, url, domain):
    percentage = 0
    i = 0
    unsafe = 0
    for a in soup.find_all('a', href=True):
        if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (
                url in a['href'] or domain in a['href']):
            unsafe = unsafe + 1
        i = i + 1

    try:
        percentage = unsafe / float(i) * 100
    except:
        return 1

    if percentage < 31.0:
        return 1
    elif (percentage >= 31.0) and (percentage < 67.0):
        return 0
    else:
        return -1


# Links_in_tags
def links_in_tag(soup, url, domain):
    i = 0
    success = 0
    if soup == -999:
        return -1
    else:
        for link in soup.find_all('link', href=True):
            dots = [x.start(0) for x in re.finditer('\.', link['href'])]
            if url in link['href'] or domain in link['href'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        for script in soup.find_all('script', src=True):
            dots = [x.start(0) for x in re.finditer('\.', script['src'])]
            if url in script['src'] or domain in script['src'] or len(dots) == 1:
                success = success + 1
            i = i + 1
        try:
            percentage = success / float(i) * 100
        except:
            return 1

        if percentage < 17.0:
            return 1
        elif (percentage >= 17.0) and (percentage < 81.0):
            return 0
        else:
            return -1


# SFH
def sfh(soup, url, domain):
    if len(soup.find_all('form', action=True)) == 0:
        return 1
    else:
        for form in soup.find_all('form', action=True):
            if form['action'] == "" or form['action'] == "about:blank":
                return -1
            elif url not in form['action'] and domain not in form['action']:
                return 0
            else:
                return 1


# Submitting to email
def submit_to_email(url):
    return -1 if re.findall(r"[mail\(\)|mailto:?]", url) else 1


# Abnormal URL
def abnormal_URL(url):
    response = requests.get(url)
    if response == "":
        return -1
    else:
        if response.text == whois.get(url):
            return 1
        else:
            return -1


# Redirect
def redirect(url):
    response = requests.get(url)
    if response == "":
        return -1
    else:
        if len(response.history) <= 1:
            return -1
        elif len(response.history) <= 4:
            return 0
        else:
            return 1


def hide_status_bar_mouseover(soup):
    return 1 if re.findall("<script>.+onmouseover.+</script>", str(soup)) else -1


def disable_right_click(soup):
    return 1 if re.findall(r"event.button ?== ?2", str(soup)) else -1


# pop up window
def pop_up_window(soup):
    return 1 if re.findall(r"alert\(", str(soup)) else -1


def i_frame(soup):
    return 1 if re.findall(r"<iframe>", str(soup)) else -1


def domain_age(domain_name):
    try:
        whois_response = whois.whois(domain_name)
        creation_date = whois_response.creation_date
        try:
            if len(creation_date):
                creation_date = creation_date[0]
        except:
            pass

        today_date = date.today()
        age = (today_date.year - creation_date.year) * 12 + (today_date.month - creation_date.month)
        if age >= 6:
            return -1
        return 1
    except:
        return 1


def DNSRecording(domain_name_dns):
    try:
        creation_date = whois.whois(domain_name_dns).creation_date
        try:
            if len(creation_date):
                creation_date = creation_date[0]
        except:
            pass
    
        today = date.today()
        age = (today.year - creation_date.year) * 12 + (today.month - creation_date.month)
        if age >= 6:
            return 0
        return 1
    except:
        return 1


def web_traffic(url):
    try:
        rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(),
                             "xml").find("REACH")['RANK']
        return 1 if int(rank) < 100000 else 0
    except:
        return -1


# page rank
def page_Rank(url):
    try:
        rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(),
                             "xml").find("REACH")['RANK']
        if 0 < int(rank) < 100000:
            return -1
        else:
            return 1
    except:
        return 1


# google index
def google_index(url):
    site = search(url, 5)
    if site:
        return 1
    else:
        return -1


# links pointing to page
def links_pointing_to_page(soup):
    number_of_links = 0
    if re.findall(r"<a href=", str(soup)):
        number_of_links += 1
    if number_of_links == 0:
        return 1
    elif number_of_links <= 2:
        return 0
    else:
        return -1


# statistical report
def statistical_report(url, domain):
    url_match = re.search(
        'at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly', url)
    try:
        ip_address = socket.gethostbyname(domain)
        ip_match = re.search(
            '146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
            '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
            '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
            '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
            '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
            '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',
            ip_address)
        if url_match:
            return -1
        elif ip_match:
            return -1
        else:
            return 1
    except:
        print('Could not connect')
        

def get_hostname_from_url(url):
    parsed_url = urlparse(url)
    obtained_domain_name = parsed_url.netloc
    return obtained_domain_name


def get_URL():
    with open(phishing_urls_file, 'r', encoding='utf-8') as f_input:
        URL_List_Contents = f_input.readlines()
        my_obtained_phishing_URLs = []

        for URL in range(len(URL_List_Contents)):
            my_obtained_phishing_URLs.append(URL)
    return URL_List_Contents


def write_heading_to_csv_file():
    with open(phishing_features_file_path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(
            ['having_IPhaving_IP_Address', 'URLURL_Length', 'Shortining_Service', 'having_At_Symbol',
             'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State',
             'Domain_registeration_length', 'Favicon', 'port', 'HTTPS_token', 'Request_URL', 'URL_of_Anchor',
             'Links_in_tags', 'SFH', 'Submitting_to_email', 'Abnormal_URL', 'Redirect', 'on_mouseover', 'RightClick',
             'popUpWidnow', 'Iframe', 'age_of_domain', 'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index',
             'Links_pointing_to_page', 'Statistical_report', 'Result'])


def write_features_values_to_csv_file(feature_set_list):
    with open(phishing_features_file_path, 'a', encoding='utf-8', newline='') as f_features:
        writer = csv.writer(f_features)

        writer.writerow(feature_set_list)


def extract_all_features_from_url_and_content():
    print("----------------------------------------------------")
    print("Adding header file to csv file")
    write_heading_to_csv_file()
    get_generated_URL = get_URL()
    print('Total scanned URLs: ' + str(len(get_generated_URL)))
    print(get_generated_URL)
    for i in range(len(get_generated_URL)):
        final_feature_values = []
        print(get_generated_URL[i])
        phishing_URL_length = len(get_generated_URL[i])
        phishing_URL = get_generated_URL[i][:phishing_URL_length - 1]
        domain_name_of_phishing_url = get_hostname_from_url(phishing_URL)
        print(domain_name_of_phishing_url)

        print("-----------------------DONE-----------------------------")
        print("Having IP address")
        url_with_IP = having_ip_address(domain_name_of_phishing_url)
        print(url_with_IP)
        final_feature_values.append(url_with_IP)

        print("-----------------------DONE-----------------------------")
        print("URL Length")
        url_length_value = url_length(phishing_URL)
        print(url_length_value)
        final_feature_values.append(url_length_value)

        print("-----------------------DONE-----------------------------")
        print("Tiny URL")
        url_with_tiny_url = tiny_URL(phishing_URL)
        print(url_with_tiny_url)
        final_feature_values.append(url_with_tiny_url)

        print("-----------------------DONE-----------------------------")
        print("Has @ symbol")
        url_with_at_symbol = having_at_symbol(domain_name_of_phishing_url)
        print(url_with_at_symbol)
        final_feature_values.append(url_with_at_symbol)

        print("-----------------------DONE-----------------------------")
        print("Redirection")
        url_with_redirection = double_slash_redirecting(phishing_URL)
        print(url_with_redirection)
        final_feature_values.append(url_with_redirection)

        print("-----------------------DONE-----------------------------")
        print("Prefix or Suffix using hyphens")
        url_with_prefix_and_suffix = prefix_suffix(domain_name_of_phishing_url)
        print(url_with_prefix_and_suffix)
        final_feature_values.append(url_with_prefix_and_suffix)

        print("-----------------------DONE-----------------------------")
        print("URL Depth like: facebook.com/aboutus/code/source/index.html")
        url_with_url_depth = having_sub_domain(phishing_URL)
        print(url_with_url_depth)
        final_feature_values.append(url_with_url_depth)

        print("-----------------------DONE-----------------------------")
        print("URL SSL Final State")
        ssl_final_state = SSL_final_state(phishing_URL)
        print(ssl_final_state)
        final_feature_values.append(ssl_final_state)

        print("-----------------------DONE-----------------------------")
        print("Domain Registration Length")
        domain_registration = Domain_registration_length(phishing_URL)
        print(domain_registration)
        final_feature_values.append(domain_registration)

        print("-----------------------DONE-----------------------------")
        print("Favicon")
        write_file_name = os.path.join(write_file, str(i) + ".html")
        with open(write_file_name, 'rb') as f_input:
            contents = f_input.read()
            soup = BeautifulSoup(contents, 'html.parser')
        favicon_presence = favicon(soup, phishing_URL, domain_name_of_phishing_url)
        print(favicon_presence)
        final_feature_values.append(favicon_presence)

        print("-----------------------DONE-----------------------------")
        print("Port Number")
        port_number = port(domain_name_of_phishing_url)
        print(port_number)
        final_feature_values.append(port_number)

        print("-----------------------DONE-----------------------------")
        print("HTTPS token")
        url_with_https = https_token(phishing_URL)
        print(url_with_https)
        final_feature_values.append(url_with_https)

        print("-----------------------DONE-----------------------------")
        print("Request URL")
        write_file_name = os.path.join(write_file, str(i) + ".html")
        with open(write_file_name, 'rb') as f_input:
            contents = f_input.read()
            soup = BeautifulSoup(contents, 'html.parser')
        request_url_presence = request_URL(soup, phishing_URL, domain_name_of_phishing_url)
        print(request_url_presence)
        final_feature_values.append(request_url_presence)

        print("-----------------------DONE-----------------------------")
        print("URL in Anchor")
        write_file_name = os.path.join(write_file, str(i) + ".html")
        with open(write_file_name, 'rb') as f_input:
            contents = f_input.read()
            soup = BeautifulSoup(contents, 'html.parser')
        url_in_anchor = URL_of_Anchor(soup, phishing_URL, domain_name_of_phishing_url)
        print(url_in_anchor)
        final_feature_values.append(url_in_anchor)

        print("-----------------------DONE-----------------------------")
        print("Links in Tag")
        write_file_name = os.path.join(write_file, str(i) + ".html")
        with open(write_file_name, 'rb') as f_input:
            contents = f_input.read()
            soup = BeautifulSoup(contents, 'html.parser')
        links_in_tags_presence = links_in_tag(soup, phishing_URL, domain_name_of_phishing_url)
        print(links_in_tags_presence)
        final_feature_values.append(links_in_tags_presence)

        print("-----------------------DONE-----------------------------")
        print("SFH")
        write_file_name = os.path.join(write_file, str(i) + ".html")
        with open(write_file_name, 'rb') as f_input:
            contents = f_input.read()
            soup = BeautifulSoup(contents, 'html.parser')
        sfh_presence = sfh(soup, phishing_URL, domain_name_of_phishing_url)
        print(sfh_presence)
        final_feature_values.append(sfh_presence)

        print("-----------------------DONE-----------------------------")
        print("EMail Submit")
        email_submission = submit_to_email(phishing_URL)
        print(email_submission)
        final_feature_values.append(email_submission)

        print("-----------------------DONE-----------------------------")
        print("Abnormal URL")
        abnormal_url_flag = abnormal_URL(phishing_URL)
        print(abnormal_url_flag)
        final_feature_values.append(abnormal_url_flag)

        print("-----------------------DONE-----------------------------")
        print("Redirect")
        redirect_in_url = redirect(phishing_URL)
        print(redirect_in_url)
        final_feature_values.append(redirect_in_url)

        print("----------------------------------------------------")
        print("Hide Status Bar")
        write_file_name = os.path.join(write_file, str(i) + ".html")
        with open(write_file_name, 'rb') as f_input:
            contents = f_input.read()
            soup = BeautifulSoup(contents, 'html.parser')
        url_with_no_status_address = hide_status_bar_mouseover(soup)
        print(url_with_no_status_address)
        final_feature_values.append(url_with_no_status_address)

        print("----------------------------------------------------")
        print("Disabled right click")
        write_file_name = os.path.join(write_file, str(i) + ".html")
        with open(write_file_name, 'rb') as f_input:
            contents = f_input.read()
            soup = BeautifulSoup(contents, 'html.parser')
        url_with_no_right_click = disable_right_click(soup)
        print(url_with_no_right_click)
        final_feature_values.append(url_with_no_right_click)

        print("----------------------------------------------------")
        print("Popup presence")
        write_file_name = os.path.join(write_file, str(i) + ".html")

        with open(write_file_name, 'rb') as f_input:
            contents = f_input.read()
            soup = BeautifulSoup(contents, 'html.parser')
        pop_up_presence = pop_up_window(soup)
        print(pop_up_presence)
        final_feature_values.append(pop_up_presence)

        print("-----------------------DONE-----------------------------")
        print("IFrame presence")
        write_file_name = os.path.join(write_file, str(i) + ".html")

        with open(write_file_name, 'rb') as f_input:
            contents = f_input.read()
            soup = BeautifulSoup(contents, 'html.parser')
            content_with_iframe = i_frame(soup)
            print(content_with_iframe)
            final_feature_values.append(content_with_iframe)

        print("-----------------------DONE-----------------------------")
        print("Domain Age")
        url_with_domain_age = domain_age(domain_name_of_phishing_url)
        print(url_with_domain_age)
        final_feature_values.append(url_with_domain_age)

        print("-----------------------DONE-----------------------------")
        print("DNS record")
        domain_dns = DNSRecording(domain_name_of_phishing_url)
        print(domain_dns)
        final_feature_values.append(domain_dns)

        print("-----------------------DONE-----------------------------")
        print("Web Traffic")
        url_web_traffic = web_traffic(domain_name_of_phishing_url)
        print(url_web_traffic)
        final_feature_values.append(url_web_traffic)

        print("-----------------------DONE-----------------------------")
        print("Page Rank")
        page_rank_value = page_Rank(phishing_URL)
        print(page_rank_value)
        final_feature_values.append(page_rank_value)

        print("-----------------------DONE-----------------------------")
        print("Google Index")
        google_index_value = google_index(phishing_URL)
        print(google_index_value)
        final_feature_values.append(google_index_value)

        print("-----------------------DONE-----------------------------")
        print("Links pointing in page")
        write_file_name = os.path.join(write_file, str(i) + ".html")

        with open(write_file_name, 'rb') as f_input:
            contents = f_input.read()
            soup = BeautifulSoup(contents, 'html.parser')
        links_pointing_in_page_value = links_pointing_to_page(soup)
        print(links_pointing_in_page_value)
        final_feature_values.append(links_pointing_in_page_value)

        print("-----------------------DONE-----------------------------")
        print("Statistical Report")
        statistical_report_value = statistical_report(legitimate_URL, domain_name_of_phishing_url)
        print(statistical_report_value)
        final_feature_values.append(statistical_report_value)

        print("----------------------------------------------------")
        print("For Label we mark legitimate as we assume that it was hosted")
        final_feature_values.append(-1)
        print(final_feature_values)

        print("----------------------------------------------------")
        print("Writing feature values to CSV file")
        write_features_values_to_csv_file(final_feature_values)


if __name__ == '__main__':
    extract_all_features_from_url_and_content()
