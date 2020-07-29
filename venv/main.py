import os
import sqlite3 as sql
import threading
import time

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
# import android.os.Environment
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import rgba


class ImageButton(ButtonBehavior, Image):
    pass
class Mainwindow(BoxLayout):
    update_indicator = ObjectProperty(None)
class MyWid(BoxLayout):
    one = ObjectProperty(None)
    two = ObjectProperty(None)
    three=ObjectProperty(None)
class ScanWindow(FloatLayout):
    result_button=ObjectProperty(None)
    gif = ObjectProperty(None)
class ScanWindowOutput(FloatLayout):
    pass
class ShowResult(BoxLayout):
    pass
class BackWindow(BoxLayout):
    pass
class HelpWindow(BoxLayout):
    pass
class uiApp(App):
    def exit(self):
        try:
            if self.successfully_scan==True:
                con = sql.connect('athenadb.db')
                cur = con.cursor()
                cur.execute("""Drop table Main""")
                cur.execute("""Alter TABLE Rough RENAME TO Main""")

                con.commit()
                con.close()
                print("second Done!!")


        except:
            pass
        App.get_running_app().stop()
    def scan(self,var):
        lis3 = []
        var = var
        if var == 0:
            try:
                con = sql.connect('athenadb.db')
                cur = con.cursor()
                cur.execute("""Delete from main""")
                con.commit()
                con.close()
                print("Done!!")
            except:
                print("couldn't deleted!!")
        if var == 1:
            self.successfully_scan = False
            self.scanwindowscreen.result_button.disabled = True
            self.scanwindowscreen.result_button.opacity = 0
        else:
            self.successfully_updated = False

            ############### solve here ##############
            self.mainscreen.update_indicator.background_color= rgba(255,0,0)

            ############################################
        thread1 = threading.Thread(target=self.traverser_init,args=('/storage/emulated/0',lis3,var))
        thread1.start()


    def traverser_init(self,path,lis3,var):
        self.traverser(path,lis3,var)
        print('done scnnnin')
        ########################### Again changing the color of update button to original color
        self.mainscreen.update_indicator.background_color = rgba(0, 0, 255)




    def traverser(self,path,lis3,var):
        if var == 1:
            self.scanwindowscreen.result_button.opacity = 0
            self.scanwindowscreen.gif.opacity = 1
        self.func(path,lis3,var)

        if self.scanwindowscreen.result_button.opacity == 0 and var == 1:
            self.successfully_scan = True
            self.scanwindowscreen.result_button.disabled = False
            self.scanwindowscreen.result_button.opacity = 1
            self.scanwindowscreen.gif.opacity = 0
        if var == 0:
            self.successfully_updated = True


    def func(self,path, lis3, var):
        var = var

        dirs = list()
        try:

            path1, dirs1, files = next(os.walk(path))
        except:
            return 0
        for i in dirs1:
            m = path + "/" + i
            try:

                path1, dirs2, files2 = next(os.walk(m))
                dirs.append(i)
            except:
                continue

        if path not in lis3:
            lis3.append(path)
            try:
                file_stats = os.path.getsize(path)
                # size = file_stats / (1024 * 1024)
                size = round(file_stats, 4)
            except:
                size = 0
            self.adddata(path,path,size,var)
            print(path)

        else:
            pass

        if len(dirs) == 0 and len(files) == 0:
            str = path
            str1 = list(str[::-1])
            lis2 = list()
            ctr = 0
            for i in str1:
                if i != '/' and ctr == 0:

                    pass
                elif (ctr == 1):
                    lis2.append(i)
                elif i == '/':

                    ctr += 1


                else:
                    pass
            lis2 = ''.join(lis2)
            lis2 = lis2[::-1]
            path = lis2
            self.func(path, lis3,var)
        else:
            if len(files) != 0:
                for i in files:
                    m = path + "/" + i
                    if m not in lis3:
                        lis3.append(m)
                        try:
                            file_stats = os.path.getsize(m)
                            #size = file_stats / (1024 * 1024)
                            size = round(file_stats,4)
                        except:
                            size = 0
                        self.adddata(m, i, size,var)
                        print(m)


                    else:

                        continue
            else:
                pass
            if len(dirs) != 0:
                for i in dirs:
                    m = path + "/" + i
                    if i == "__pycache__":
                        continue
                    if m not in lis3:

                        lis3.append(m)
                        try:
                            file_stats = os.path.getsize(m)
                            # size = file_stats / (1024 * 1024)
                            size = round(file_stats, 4)
                        except:
                            size = 0
                        self.adddata(m, i, size,var)
                        print(m)

                        self.func(m, lis3,var)
                    else:
                        str = m
                        str1 = list(str[::-1])
                        lis2 = list()
                        ctr = 0
                        for j in str1:
                            if j != '/' and ctr == 0:

                                pass
                            elif (ctr == 1):
                                lis2.append(j)
                            elif j == '/':

                                ctr += 1


                            else:
                                pass
                        lis2 = ''.join(lis2)
                        lis2 = lis2[::-1]
                        path = lis2
                        continue

    def ScanWindowOutputScreen_to_ShowResultScreen_for_dup_data(self):
        self.previous_screen = str(self.screen_manager.current)
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'showresultscreen'
        self.get_duplicate_data()
        ###################################### currently use less ####################
    '''def ScanWindowOutputScreen_to_ShowResultScreen(self):
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'showresultscreen'
        self.getdata()'''
        ########################################################
    def mainscreen_to_scanwindowscreen(self):
        self.screen_manager.transition.direction = 'up'
        self.screen_manager.current = 'scanwindowscreen'


        try:
            con = sql.connect('athenadb.db')
            cur = con.cursor()
            cur.execute("""CREATE TABLE ROUGH ( address text, name text, size int)""")
            con.commit()
            con.close()
            print("second Done!!")

        except:
            print("second Table is already here")
        self.scan(1)

    def making_records_for_rough_table(self,a,b,c):
        con = sql.connect('athenadb.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO rough (ADDRESS, NAME ,SIZE ) VALUES (?,?,?)""", (a, b, c))
        con.commit()
        con.close()
    def adddata(self,a,b,c,var):
        if var == 0:######################### means updating record##############################
            con = sql.connect('athenadb.db')
            cur = con.cursor()
            cur.execute("""INSERT INTO MAIN (ADDRESS, NAME ,SIZE ) VALUES (?,?,?)""",(a,b,c))
            con.commit()
            con.close()
        else:  ########################### adding data to rough table while scanning #######################
            con = sql.connect('athenadb.db')
            cur = con.cursor()
            cur.execute("""INSERT INTO Rough (ADDRESS, NAME ,SIZE ) VALUES (?,?,?)""", (a, b, c))
            con.commit()
            con.close()
    def mainscreen_to_resultscreen_for_large_data(self):
        self.previous_screen = str(self.screen_manager.current)
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = 'showresultscreen'
        self.get_large_files()
    def ScanWindowOutputScreen_to_ShowResultScreen_for_new_data(self):
        self.previous_screen = str(self.screen_manager.current)
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'showresultscreen'
        self.get_new_files()
    def ScanWindowOutputScreen_to_ShowResultScreen_for_removed_data(self):
        self.previous_screen = str(self.screen_manager.current)
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = 'showresultscreen'
        self.get_removed_files()
    def get_removed_files(self):
        con = sql.connect('athenadb.db')
        cur = con.cursor()
        cur.execute("""SELECT * FROM Main
WHERE (address,name,size) NOT IN
( SELECT *
  FROM Rough
) """)
        dat = cur.fetchall()
        con.commit()
        con.close()
        self.state = True
        thread7 = threading.Thread(target=self.show_removed_data_at_ui, args=(dat,))
        thread7.start()
    def show_removed_data_at_ui(self,dat):
        time.sleep(0.5)
        for i in dat:
            if 1 == 1:
                if self.state == False:
                    break
                print(i)
                b = MyWid()
                b.one.text += i[0]

                b.two.text += str(i[1])
                b.three.text += str(i[2]) + ' bytes'
                self.showresultscreen.lay.add_widget(b)

                time.sleep(0.3)
        print('chala')
    def get_new_files(self):

        con = sql.connect('athenadb.db')
        cur = con.cursor()
        cur.execute("""SELECT * FROM Rough
WHERE (address,name,size) NOT IN
( SELECT *
  FROM Main
) """)
        dat = cur.fetchall()
        con.commit()
        con.close()
        self.state = True
        thread6 = threading.Thread(target=self.show_new_data_at_ui, args=(dat,))
        thread6.start()
    def show_new_data_at_ui(self,dat):
        time.sleep(0.5)
        for i in dat:
            if 1 == 1:
                if self.state == False:
                    break
                print(i)
                b = MyWid()
                b.one.text += i[0]

                b.two.text += str(i[1])
                b.three.text += str(i[2]) + ' bytes'
                self.showresultscreen.lay.add_widget(b)

                time.sleep(0.3)
        print('chala')
    def get_large_files(self):
        con = sql.connect('athenadb.db')
        cur = con.cursor()
        cur.execute("""select * from Rough where size>1073741824""")
        dat = cur.fetchall()
        con.commit()
        con.close()
        self.state = True
        thread4 = threading.Thread(target=self.show_large_data_at_ui, args=(dat,))
        thread4.start()
    def show_large_data_at_ui(self,dat):
        time.sleep(0.2)
        for i in dat:
            if 1==1:
                if self.state == False:
                    break
                print(i)
                b = MyWid()
                b.one.text+=i[0]

                b.two.text += str(i[1])
                b.three.text+=str(i[2])+' bytes'
                self.showresultscreen.lay.add_widget(b)

                time.sleep(0.2)
        print('chala')
    def ScanWindowOutputScreen_to_ShowResultScreen_for_threats(self):
        self.previous_screen = str(self.screen_manager.current)
        self.screen_manager.transition.direction = 'down'
        self.screen_manager.current = 'showresultscreen'

        self.get_threats()
    def get_threats(self):
        con = sql.connect('athenadb.db')
        cur = con.cursor()
        cur.execute("""SELECT 
    name,size,address,
    COUNT(*) occurrences
FROM Rough
GROUP BY
    name,size
HAVING 
    COUNT(*) > 60""")
        dat = cur.fetchall()
        con.commit()
        con.close()
        self.state = True
        thread5 = threading.Thread(target=self.show_malicious_data_at_ui, args=(dat,))
        thread5.start()
    def show_malicious_data_at_ui(self,dat):
        time.sleep((0.5))
        for i in dat:
            if self.state ==False:
                break
            if 'emulated/0/' in str(i[2]):
                #print(i)
                b = MyWid()
                b.one.text='Total Copies: '+str(i[3])

                b.two.text += str(i[0])
                b.three.text += str(i[1]) + ' bytes'
                self.showresultscreen.lay.add_widget(b)
                time.sleep(0.3)
        #print('chala')

    def get_duplicate_data(self):
        con = sql.connect('athenadb.db')
        cur = con.cursor()
        cur.execute("""SELECT address,name,size
FROM (
  SELECT address,name,size,
         COUNT(*) OVER (PARTITION BY name) AS cnt
  FROM Rough) AS t
WHERE t.cnt > 1""")
        dat = cur.fetchall()
        con.commit()
        con.close()
        self.state = True
        thread3 = threading.Thread(target=self.show_duplicate_data_at_ui, args=(dat,))
        thread3.start()
    def show_duplicate_data_at_ui(self,dat):
        for i in dat:
            if self.state == False:
                break
            if i[3].startswith(''):
                print(i)
                b = MyWid()
                b.one.text+=i[0]

                b.two.text += str(i[1])
                b.three.text += str(i[2]) + ' bytes'
                self.showresultscreen.lay.add_widget(b)

                time.sleep(0.3)



    def build(self):
        self.screen_manager = ScreenManager()
        try:
            con = sql.connect('athenadb.db')
            cur = con.cursor()

            cur.execute("""Drop table ROUGH""")
            con.commit()
            con.close()


        except:
            pass
        self.mainscreen = Mainwindow()
        screen = Screen(name='mainscreen')
        screen.add_widget(self.mainscreen)
        self.screen_manager.add_widget(screen)

        self.showresultscreen = ShowResult()
        screen = Screen(name='showresultscreen')
        screen.add_widget(self.showresultscreen)
        self.screen_manager.add_widget(screen)

        self.scanwindowscreen = ScanWindow()
        screen = Screen(name='scanwindowscreen')
        screen.add_widget(self.scanwindowscreen)
        self.screen_manager.add_widget(screen)

        self.scanwindowsoutputscreen = ScanWindowOutput()
        screen = Screen(name='scanwindowoutputscreen')
        screen.add_widget(self.scanwindowsoutputscreen)
        self.screen_manager.add_widget(screen)

        self.backwindowscreen = BackWindow()
        screen = Screen(name='backwindowscreen')
        screen.add_widget(self.backwindowscreen)
        self.screen_manager.add_widget(screen)

        self.helpwindowscreen = HelpWindow()
        screen = Screen(name='helpwindowscreen')
        screen.add_widget(self.helpwindowscreen)
        self.screen_manager.add_widget(screen)



        try:
            con = sql.connect('athenadb.db')
            cur = con.cursor()
            cur.execute("""CREATE TABLE MAIN ( address text, name text, size int)""")
            con.commit()
            con.close()
            print("Done!!")
        except:
            print("Table is already here")



        return self.screen_manager
    def back_from_scanwindow_output_screen_to_mainscreen(self):
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'backwindowscreen'
    def hello(self):
        if self.scanwindowscreen.result_button.opacity == 1:

            self.scanwindowscreen_to_scanwindowoutputscreen()
    def scanwindowscreen_to_scanwindowoutputscreen(self):
        self.screen_manager.transition.direction = 'up'
        self.screen_manager.current = 'scanwindowoutputscreen'
    def yes_on_scanwindow(self):
        try:
            if self.successfully_scan == True:
                con = sql.connect('athenadb.db')
                cur = con.cursor()
                cur.execute("""Drop table Main""")
                cur.execute("""Alter TABLE Rough RENAME TO Main""")

                con.commit()
                con.close()
                print("Done!!")
                try:
                    con = sql.connect('athenadb.db')
                    cur = con.cursor()
                    cur.execute("""CREATE TABLE ROUGH ( address text, name text, size int)""")
                    con.commit()
                    con.close()
                    print("second Done!!")

                except:
                    print("second Table is already here")




        except:
            content = Button(text='Some problem occured  with database!!' + '\n\n                  Close')

            popup = Popup(title='Warning!!:\n\n', content=content, auto_dismiss=False)

            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)

            # open the popup
            popup.open()
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'mainscreen'
    def no_on_scanwindow(self):
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = 'scanwindowoutputscreen'
    def back_on_showresultscreen(self):
        self.state = False
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = self.previous_screen
    def mainscreen_to_helpwindow(self):
        self.screen_manager.transition.direction = 'up'
        self.screen_manager.current = 'helpwindowscreen'
    def helpwindow_to_mainscreen(self):
        self.screen_manager.transition.direction = 'down'
        self.screen_manager.current = 'mainscreen'
if __name__ == '__main__':


    LabelBase.register(name='Modern Pictograms',
                       fn_regular='modernpics.ttf')
    LabelBase.register(name='second',
                       fn_regular='FFF_Tusj.ttf')

    LabelBase.register(name='third',
                       fn_regular='GrandHotel-Regular.ttf')
    uiApp().run()
