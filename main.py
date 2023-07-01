import requests
from instagrapi import Client
import imageio
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import schedule
import time

class Node:
    def __init__(self,value):
        self.Value = value
        self.url = None
        self.next = None
        
        
class ApiInstagram:
    def __init__(self):
        self.client = Client()
        with open('instagram_authentication.txt','r') as f:
            self.username, self.password = f.read().splitlines()
        with open('Email_authentication.txt.txt','r') as f :
            self.smtp_username, self.smtp_password = f.read().splitlines()
        self.Hashtags = ["تلاوة", "تجويد", "قراءة", "التجويد", "مقامات", "مقام", "المد", "الصوت", "الحروف", "السورة", "الآية", "سورة", "الترتيل", "المعاني", "المفردات", "تجويد", "تدبر", "التفسير", "المصحف", "حفظ", "التدبر", "ترتيل", "القرآن_الكريم", "القراءة", "المدرسة_القرآنية", "المدرسة_القرآنية", "الترتيل", "تلاوة_القرآن", "تلاوة_مجودة", "تجويد", "الحفظ", "تفسير_القرآن", "تجويد_القرآن", "قراءة_القرآن", "المصحف_الشريف", "حفظ_القرآن", "المعجم_القرآني", "التفسير_الميسر", "التجويد_المتقن", "قراءة_المفردات", "تلاوة_ترتيلية", "حفظ_القرآن_الكريم", "تدبر_آيات_القرآن", "التدبر_في_القرآن", "قراءة_القرآن_الكريم", "تجويد_القرآن_الكريم", "التفسير_القرآني", "تدبر_كلمات_القرآن", "التدبر_في_المعاني", "التلاوة_التجويدية", "تدبر_سور_القرآن", "تجويد_المصحف_الشريف", "تدبر_الآيات_المفردات"]
        self.Words = ['اكتب شيئًا يُؤجَر عليه في الآخرة.','أكتب شيئًا يَزِد في ميزان حسناتك.','اكتب كلمة طيبة لتُسعِد قلب المؤمنين.','أكتب دعاءًا صالحًا لأحد الأشخاص الذين تحبهم في الله.',]
        self.Top = None
        self.length = 0
        self.sender_email = 'EMAIL_HOST_USER'
        self.receiver_email = 'Your Email'
        self.Login()
    def Login(self):
        try:
            self.client.login(self.username, self.password)
            print("Login successful!")
            return True
        except Exception as e:
            print(e)
            # Handle checkpoint challenge if necessary
            print("Checkpoint challenge required")
            return False
        
    def download_video(self,url):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open('Video.mp4', 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    
    def post_reel(self,caption):
        self.client.clip_upload('Video.mp4',caption)
        return True
    
    def Send_EmailNew(self,url):

        subject = 'Instagram New Post Info'
        body = f'The Video Is Now published Time is {datetime.now()} UrlVideo: {url}'
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = self.receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Start TLS encryption
            server.starttls()
            # Login to the SMTP server
            server.login(self.smtp_username, self.smtp_password)
            # Send the email
            server.send_message(message)
            # Disconnect from the server
            server.quit()
        
    def Send_EmailOld(self):
        UserID= self.client.user_id_from_username('i3oma')
        NewPost = self.client.user_clips(UserID,amount=1)
        subject = 'Instagram Old Post Info'
        body = f'The Video Is Now published Time is {datetime.now()}\n Likes: {NewPost[0].like_count}, Comments:{NewPost[0].comment_count} Views: {NewPost[0].play_count}'
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = self.receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Start TLS encryption
            server.starttls()
            # Login to the SMTP server
            server.login(self.smtp_username, self.smtp_password)
            # Send the email
            server.send_message(message)
            # Disconnect from the server
            server.quit()


    def GetNewPost(self,UserGet):
        current = self.Top
        UserName = self.client.user_id_from_username(UserGet)
        NewPost = self.client.user_clips(UserName,amount=1)
        if self.Top == None:
            self.Top = Node(NewPost[0].pk)
            self.Top.url = NewPost[0].video_url
            self.download_video(self.Top.url)
            self.Send_EmailOld()
            self.Send_EmailNew(self.Top.url)
            self.MakeLikeAndComment(NewPost[0].id)
            self.MakeStory()
            self.post_reel(NewPost[0].caption_text)
            return True
        else:
            print(NewPost[0].pk)
            print(current.Value)
            
            if current.Value == NewPost[0].pk:
                return False
            else:
                NewNode = Node(NewPost[0].pk)
                NewNode.next = self.Top
                NewNode.url = NewPost[0].video_url
                self.Top = NewNode
                self.download_video(self.Top.url)
                self.MakeLikeAndComment(NewPost[0].id)
                self.post_reel(NewPost[0].caption_text)
                self.Send_EmailOld()
                self.Send_EmailNew(self.Top.url)
                self.MakeStory()
                return True
            
    def MakeLikeAndComment(self,id):
        comment = [f'#{random.choice(self.Hashtags)}' for i in range(0,random.randint(2,5))]
        comment = ' '.join(comment)
        self.client.media_like(id)
        self.client.media_comment(id,str(comment))
        return True
    
    def download_videoStory(self,url):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open('Sotrys.mp4', 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
    def MakeStory(self):
        UserID= self.client.user_id_from_username('i3oma')
        Storyes = self.client.user_stories(UserID,amount=0)
        for Story in Storyes:
            if Story.media_type == 2:
                self.download_videoStory(Story.video_url)
                self.client.video_upload_to_story('Sotrys.mp4')
                return True
                
    
       
API_Start = ApiInstagram()
def Job():
    API_Start.GetNewPost('i3oma')

    
schedule.every().day.at("19:12").do(Job)
while True:
    schedule.run_pending()
    time.sleep(1)   
    
























  
 

    
    
       



