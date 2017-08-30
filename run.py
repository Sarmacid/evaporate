#!/usr/bin/env python

from evaporate import yt, db, e_xml


def main():
    db.create_db()
    yt.get_missing_episodes()
    e_xml.generate_xml()


if __name__ == "__main__":
    main()
