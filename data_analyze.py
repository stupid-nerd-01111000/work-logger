import pandas as pd
from datetime import datetime

class AttendanceAnalyzer:
    def __init__(self, logs_file, registration_file):
        self.logs_file = logs_file
        self.registration_file = registration_file
        self.work_start = datetime.strptime("08:30:00", "%H:%M:%S").time()
        self.work_end = datetime.strptime("17:30:00", "%H:%M:%S").time()

    def reload_data(self):
        self.logs_df = pd.read_csv(self.logs_file)
        self.registration_df = pd.read_csv(self.registration_file)

    def analyze_date(self, target_date):
        # Reload data to include the latest updates
        self.reload_data()

        daily_logs = self.logs_df[self.logs_df["date"] == target_date]
        present_users = set(daily_logs["user_id"])
        all_users = set(self.registration_df["user_id"])
        absent_users = all_users - present_users

        late_early_data = []
        for user_id in present_users:
            user_logs = daily_logs[daily_logs["user_id"] == user_id]
            enter_logs = user_logs[user_logs["enter_or_exit"] == "enter"]
            exit_logs = user_logs[user_logs["enter_or_exit"] == "exit"]

            first_entry_time = (
                datetime.strptime(enter_logs["time"].min(), "%H:%M:%S").time()
                if not enter_logs.empty
                else None
            )
            last_exit_time = (
                datetime.strptime(exit_logs["time"].max(), "%H:%M:%S").time()
                if not exit_logs.empty
                else None
            )

            late_minutes = 0
            early_minutes = 0

            if first_entry_time and first_entry_time > self.work_start:
                late_minutes = (datetime.combine(datetime.today(), first_entry_time) -
                                datetime.combine(datetime.today(), self.work_start)).seconds // 60

            if last_exit_time and last_exit_time < self.work_end:
                early_minutes = (datetime.combine(datetime.today(), self.work_end) -
                                 datetime.combine(datetime.today(), last_exit_time)).seconds // 60

            late_early_data.append({
                "user_id": user_id,
                "late_minutes": late_minutes,
                "early_minutes": early_minutes,
            })

        return {
            "absent_users": absent_users,
            "late_early_data": late_early_data,
        }
