from PIL import Image
from telebot import TeleBot
import telebot
from PIL import Image
import os
def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        w, h = img.size
    return {'w': w, 'h':h}


def resize_image(image_path, width, height, output_path):
    
    with Image.open(image_path) as image:
        
        resized_image = image.resize((width, height), resample=Image.BOX)
        
        resized_image.save(output_path)
    
    return True
# bot token here
bot  = TeleBot('####', num_threads=20, skip_pending=True)

@bot.message_handler(commands=['start'])
def start(message):
  k = '''
👋🏻꒐ اهلا بك في  بوت تغيير حجم الصور!
⏺꒐ قم بأرسال الصورة الان، وأتبع تعليمات البوت!
⎯ ⎯ ⎯ ⎯
  '''
  bot.reply_to(message, k)
@bot.message_handler(content_types=['photo'])
def rex(message):
  fileid = message.photo[-1].file_id
  d = bot.download_file(bot.get_file(fileid).file_path)
  with open('temp.jpg', 'wb') as o:
    o.write(d)
  q = get_image_dimensions('temp.jpg')
  h = q['h']
  w = q['w']
  bot.reply_to(message, f'ابعاد الصورة الحالية: \n- الطول: <code>{h}px</code> \n- العرض: <code>{w}px</code> .', parse_mode='html')
  x = bot.reply_to(message, 'اوكية.. الان ارسل ابعاد لصورة المطلوب مثل:\n<strong>640x360</strong>\nانتبة يكون نفس الشيء !! ..\n', parse_mode='html')
  bot.register_next_step_handler(x, adjust, fileid)
def adjust(message, fileid):
  text = message.text
  if 'x' not in text:
    return bot.reply_to(message, 'الابعاد صيغتهم خطأ .. عيد من جديد..')
  x, y = text.split('x')
  try:
    x = int(x)
    y = int(y)
  except:
    return bot.reply_to(message, 'الابعاد لازم ارقام .')
  if int(x) <35:
    return bot.reply_to(message, f'عرض الصورة <code>{x}</code>، جدا صغير ..', parse_mode='html')
  if int(x) <10:
    return bot.reply_to(message, f'طول الصورة <code>{y}</code>، جدا صغير ..', parse_mode='html')
  d = bot.download_file(bot.get_file(fileid).file_path)
  with open("img.jpg", 'wb') as t:
    t.write(d)
  resu = resize_image('img.jpg', x, y, 'result.jpg')
  if resu:
    bot.send_document(message.chat.id, open('result.jpg', 'rb'), caption=f'الطول: <code>{y}px</code> .\nالعرض: <code>{x}px</code> .', parse_mode='html')
    return
bot.infinity_polling()
