#!/usr/bin/python
# _*_ coding: utf-8 _*_


__author__ = 'krio'

import MySQLdb
import json
import requests
import re


class SubscribePy:
    def __init__(self, login, status=None):
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="subscribepy")
        self.cur = self.db.cursor()
        self.login = login
        g = re.search(r"[\w\d.\-]+@[\w\d.\-]+", self.login)
        self.status = status
        if g:
            if status is None:
                SubscribePy.user_create(self)
            elif status == 1:
                SubscribePy.user_confirm(self)
                # SubscribePy.rambler(self, 'subscribe')
            elif status == 2:
                SubscribePy.user_unsubscribe(self)
                # SubscribePy.rambler(self, 'unsubscribe')
        else:
            print "Это не емайл"

    def user_create(self):
        try:
            query = """SELECT login FROM user WHERE login='{0}'"""
            self.cur.execute(query.format(self.login))
            result = self.cur.fetchone()
            if not result:
                query = """INSERT INTO user (login) values ('{0}');"""
                self.cur.execute(query.format(self.login))
                print "Запись создана"
            else:
                print "такой логин уже присутствует"
        except MySQLdb.Error:
            print(self.db.error())
        finally:
            self.db.commit()
            self.db.close()

    def user_confirm(self):
        try:
            query = """SELECT confirm FROM user WHERE login='{0}'"""
            self.cur.execute(query.format(self.login))
            result = self.cur.fetchone()
            if result[0] == 0:
                query = """UPDATE user SET confirm=1 WHERE login=('{0}');"""
                self.cur.execute(query.format(self.login))
                print "Вы теперь подписаны"
            else:
                print "Вы уже были подписаны"
        except MySQLdb.Error:
            print(self.db.error())
        finally:
            self.db.commit()
            self.db.close()

    def user_unsubscribe(self):
        try:
            query = """SELECT confirm FROM user WHERE login='{0}'"""
            self.cur.execute(query.format(self.login))
            result = self.cur.fetchone()
            if result[0] == 1:
                query = """UPDATE user SET confirm=0 WHERE login=('{0}');"""
                self.cur.execute(query.format(self.login))
                print "Вы отписались от рассылки"
            else:
                print "Вы уже были отписанны"
        except MySQLdb.Error:
            print(self.db.error())
        finally:
            self.db.commit()
            self.db.close()

            # def rambler(self, method):
            #     subscriptions_api_url = 'https://mail.rambler.ru/promo/api'
            #     params = {'method': 'Rambler::Mail::Subscriptions::API::' + method,
            #               'params': [{'email': self.login,
            #                           'list': 'gazeta_news'
            #                           }]
            #               }
            #     response = requests.post(subscriptions_api_url, data=json.dumps(params))
            #     if not response.ok:
            #         raise IOError, response.status_code
            #     print response.content


SubscribePy('av_aquadfsfsdf.gh')
