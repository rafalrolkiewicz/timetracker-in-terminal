"""
Simple time tracker for life and work. Runs in terminal
Featrues:
- start/stop timer
- add entry manually
- browse entries
- edit entries
- save in sqlite using sqlalchemy
"""

from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time
import threading

Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    notes = Column(String)


class TimeTracker:
    def __init__(self):
        engine = create_engine('sqlite:///timetracker.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.timer_running = False

    def start_timer(self):
        name = self.get_name()
        start_time = datetime.now()
        self.current_entry = Entry(name=name, start_time=start_time)
        self.start_time = time.time()
        self.timer_running = True
        self.timer_thread = threading.Thread(target=self.print_elapsed_time)
        self.timer_thread.start()

    def stop_timer(self):
        if not self.timer_running:
            print("No timer is currently running.")
            return
        end_time = datetime.now()
        self.current_entry.end_time = end_time
        self.current_entry.start_time = datetime.strptime(
            self.current_entry.start_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        self.current_entry.end_time = datetime.strptime(
            self.current_entry.end_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        self.session.add(self.current_entry)
        self.session.commit()
        self.timer_running = False
        self.timer_thread.join()
        elapsed_time = int(time.time() - self.start_time)
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(
            f'\r{self.current_entry.name}, Time elapsed: {hours:02}:{minutes:02}:{seconds:02}')

    def print_elapsed_time(self):
        while self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            if seconds > 1:
                print(
                    f'\r{self.current_entry.name}, Time elapsed: {hours:02}:{minutes:02}:{seconds:02}', end='')
            time.sleep(1)

    def add_entry(self, name, start_time, elapsed_time):
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        if elapsed_time:
            end_time = start_time + timedelta(minutes=int(elapsed_time))
        else:
            end_time = None
        entry = Entry(name=name,
                      start_time=start_time, end_time=end_time)
        self.session.add(entry)
        self.session.commit()

    def browse_entries(self):
        entries = self.session.query(Entry).order_by(Entry.start_time.desc())
        for entry in entries:
            if entry.end_time:
                elapsed_time = entry.end_time - entry.start_time
            else:
                elapsed_time = datetime.now() - entry.start_time
            elapsed_time = str(elapsed_time).split('.')[0]
            print(f'{"ID:":<3} {entry.id:<3} {"Name:":<5} {entry.name:<13} {"Start time:":<11} {entry.start_time.strftime("%Y-%m-%d %H:%M:%S"):<21} {"Elapsed time:":<14} {elapsed_time:<15}')
            """print(
                f'ID: {entry.id}, name: {entry.name}, Start time: {entry.start_time}, Elapsed time: {elapsed_time}')"""

    def edit_entry(self, id, name=None, start_time=None, end_time=None, notes=None):
        entry = self.session.query(Entry).filter(Entry.id == id).first()
        if name:
            entry.name = name
        if start_time:
            entry.start_time = start_time
        if end_time:
            entry.end_time = end_time
        if notes:
            entry.notes = notes
        self.session.commit()

    def get_name(self):
        names = self.session.query(Entry.name).distinct()
        names = [name[0] for name in names]
        print("Existing names:")
        for i, name in enumerate(names, start=1):
            print(f"{i}. {name}")
        print(f"{len(names) + 1}. Add new name")
        choice = input("Choose a name by number or add a new one: ")
        if choice.isdigit() and 1 <= int(choice) <= len(names):
            return names[int(choice) - 1]
        else:
            return input("Enter new name: ")

    def run(self):
        while True:
            print('')
            print('1. Start timer')
            print('2. Stop timer')
            print('3. Add entry')
            print('4. Browse entries')
            print('5. Edit entry')
            print('6. Exit')
            print('')
            choice = input('Choose an option: ')
            if choice == '1':
                self.start_timer()
            elif choice == '2':
                self.stop_timer()
            elif choice == '3':
                name = self.get_name()
                start_time = input('Enter start time (YYYY-MM-DD HH:MM:SS): ')
                elapsed_time = input('Enter duration in minutes: ')
                self.add_entry(name, start_time, elapsed_time)
            elif choice == '4':
                self.browse_entries()
            elif choice == '5':
                id = input('Enter entry id: ')
                entry = self.session.query(Entry).filter(Entry.id == id).first()
                if entry is None:
                    print(f"No entry found with id {id}")
                    continue
                name = input('Enter new name: ')
                start_time = input('Enter new start time: ')
                elapsed_time = input('Enter new elapsed time: ')
                if elapsed_time and not start_time:
                    start_time = entry.start_time
                    end_time = start_time + timedelta(minutes=int(elapsed_time))
                else:
                    end_time = None
                notes = input('Enter new notes: ')
                self.edit_entry(id, name, start_time,
                                end_time, notes)
            elif choice == '6':
                break
            else:
                print('Invalid choice')


if __name__ == '__main__':
    tracker = TimeTracker()
    tracker.run()
