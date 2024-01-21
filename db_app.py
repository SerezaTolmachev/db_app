from tkinter import *

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:0610@localhost/postgres")

Base = declarative_base()


class User(Base):
    __tablename__ = 'users2'
    id = Column(Integer, primary_key=True, nullable=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250))
    phone = Column(String(250))


Base.metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()
main_index = ()


def get_data():
    data = session.query(User).order_by(User.id).all()
    data_list = []
    for i in data:
        a = f'{i.id} {i.name} {i.email} {i.phone}'
        data_list.append(a)
    return data_list


def refresh():
    global main_index
    main_index = ()
    data = get_data()
    data_variable = Variable(value=data)
    listbox.config(listvariable=data_variable)
    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    email_entry.delete(0, END)


def delete_user():
    if main_index == ():
        print('Ошибка')
        return 1
    item = listbox.get(main_index)
    session.query(User).filter(User.id == item.split()[0]).delete()
    session.commit()
    refresh()


def add_user():
    if name_entry.get() == '':
        print('Ошибка')
        return 1
    user = User(name=name_entry.get(), phone=phone_entry.get(), email=email_entry.get())
    session.add(user)
    session.commit()
    refresh()
    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    email_entry.delete(0, END)


def set_entries(x):
    index = listbox.curselection()
    if index != ():
        global main_index
        main_index = index
        item = listbox.get(index)
        name_entry.delete(0, END)
        phone_entry.delete(0, END)
        email_entry.delete(0, END)
        name_entry.insert(END, item.split()[1])
        if len(item.split()) > 3:
            phone_entry.insert(END, item.split()[3])
        if len(item.split()) > 2:
            email_entry.insert(END, item.split()[2])


def edit_user():
    if main_index == ():
        print('Ошибка')
        return 1
    item = listbox.get(main_index)
    user = session.query(User).filter(User.id == item.split()[0]).first()
    if name_entry.get() != user.name:
        user.name = name_entry.get()
    if phone_entry.get() != user.phone:
        user.phone = phone_entry.get()
    if email_entry.get() != user.email:
        user.email = email_entry.get()
    session.commit()
    refresh()


root = Tk()

root.title('app for datab')
root.geometry('800x600')

name_label = Label(root, text='Имя')
email_label = Label(root, text='Почта')
phone_label = Label(root, text='Номер')

name_label.place(x=50, y=50)
email_label.place(x=50, y=100)
phone_label.place(x=50, y=150)

name_entry = Entry(root)
email_entry = Entry(root)
phone_entry = Entry(root)

name_entry.place(x=100, y=50)
email_entry.place(x=100, y=100)
phone_entry.place(x=100, y=150)

add_button = Button(root, text='Добавить', command=add_user)
update_button = Button(root, text='Обновить', command=refresh)
delete_button = Button(root, text='Удалить', command=delete_user)
edit_button = Button(root, text='Изменить', command=edit_user)

add_button.place(x=50, y=500)
update_button.place(x=150, y=500)
delete_button.place(x=250, y=500)
edit_button.place(x=350, y=500)


temp_data = get_data()
data_var = Variable(value=temp_data)
listbox = Listbox(listvariable=data_var, font=('Times New Roman', 15))

listbox.bind('<<ListboxSelect>>', set_entries)


listbox.place(x=100, y=250, height=200, width=400)


main_screen_button = Label(root, text='Информация')

main_screen_button.place(x=50, y=220)


root.mainloop()