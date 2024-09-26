#!/usr/bin/env python3
import unittest
from db import DB


class TestDb(unittest.TestCase):
    def setUp(self):
        self.db = DB()
        self.emails = ['me', 'he', 'them']
        self.passwords = ['me', 'he', 'them']
        users = []
        for e, p in zip(self.emails, self.passwords):
            user = self.db.add_user(e, p)
            users.append(user)
        self.users = users

    def test_new_user(self):
        from user import User
        map(lambda x: self.assertIsInstance(x, User), self.users)

    def test_retrive_user_with_invalid_email(self):
        for email in ['they', 'there', 'shit']:
            self.assertRaises(self.db.find_user_by(email=email))

    def test_retrive_user_with_valid_email(self):
        for email, user in zip(self.emails, self.users):
            self.assertEquals(user, self.db.find_user_by(email=email))


if __name__ == '__main__':
    unittest.TestCase.run()
