from flask import Blueprint, render_template, request, flash

class UserApp():
    def returnWeb():
        return render_template('user_app_main.html')