import imaplib
import email
import smtplib
import ssl
import requests

def query_chatgpt(message):
    url = 'https://api.openai.com/v1/chat/completions'
    api_key = 'Dummyjaiejfaoifjaiojefaoejfaojfioajifajofajofjaiofjaioefjaoeif'  # 自分のAPIキーに置き換えてください
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        'model': 'text-davinci-002',  # 使用するモデルを指定します
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                     {'role': 'user', 'content': message}
                     {'role': 'user', 'content': '論理的で、読みやすい文章かどうかをチェックしてください。以下のことが記載されているかどうかをチェックしてください。\n報告日\n報告者\nマネージャーが把握したい内容\nお客様の課題\n報告者の自社の競合\nお客様の予算\nお客様の決裁者\nお客様の導入時期\n報告者の次のアクション\n報告者のその日の商談における疑問点・懸念点\n報告者の次の日からの計画'}]
    }
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    # APIからのレスポンスを出力します
    print(f"Response from API: {response_data}")

    return response_data['choices'][0]['message']['content']


# メールサーバーの接続情報
imap_server = 'imap.mail.yahoo.co.jp'
imap_port = 993
imap_username = 'Dummyajefajoiefjaofjaoejfa@yahoo.co.jp'
imap_password = 'Dummyajefiajofaefhaojsfda7878979yhihiuh'

context = ssl.create_default_context()

# メールサーバーに接続
imap_conn = imaplib.IMAP4_SSL(imap_server, imap_port, ssl_context=context)
imap_conn.login(imap_username, imap_password)
imap_conn.select()

# メールの検索と取得
status, email_ids = imap_conn.search(None, '(UNSEEN SUBJECT "76321")')  # サブジェクトに"76321"を含む未読メールを検索
email_ids = email_ids[0].split()

for email_id in email_ids:
    status, email_data = imap_conn.fetch(email_id, '(BODY.PEEK[])')
    raw_email = email_data[0][1]
    email_message = email.message_from_bytes(raw_email)

    # 送信者のメールアドレスと本文を取得
    sender_email = email_message['From']
    email_body = ""

    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                email_body = part.get_payload(decode=True).decode('utf-8')
                break
    else:
        email_body = email_message.get_payload(decode=True).decode('utf-8')

    # ChatGPTに問い合わせ
    response = query_chatgpt(email_body)

    # 回答をメール送信
    smtp_server = 'smtp.mail.yahoo.co.jp'
    smtp_port = 465
    smtp_username = 'akfajdofajdfaDummyajefajoiefjaofjaoejfa@yahoo.co.jp'  # あなたのYahooメールアドレス
    smtp_password = 'dfajefoajefDummyajefajoiefjaofjaoejfa'  # Yahooメールのパスワード

    subject = 'Re: ' + email_message['Subject']
    body = f"From: {smtp_username}\nTo: {sender_email}\nSubject: {subject}\n\n{response}"

    smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
    smtp_conn.starttls()
    smtp_conn.login(smtp_username, smtp_password)
    smtp_conn.sendmail(smtp_username, sender_email, body)
    smtp_conn.quit()

# メールサーバーとの接続を終了
imap_conn.close()
imap_conn.logout()
