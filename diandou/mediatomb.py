# -*- coding:utf-8 -*-

import os
import os.path
import codecs
import sqlite3
from diandou.models import db


MEDIA_EXTENSIONS = ['.avi', '.mkv', '.rmvb']
MEDIATOMB_DATABASE_URI = 'mediatomb.db'
MEDIATOMB_SERVER_IP = ''
MEDIATOMB_SERVER_PORT = ''


class Media(db.Model):

    def __init__(self, mediatomb_id, filename, mime_type, aka):
        self.mediatomb_id = mediatomb_id
        self.filename = filename
        self.mime_type = mime_type
        self.aka = aka

    id = db.Column(db.Integer, primary_key=True)
    mediatomb_id = db.Column(db.Integer)
    filename = db.Column(db.String(126))
    mime_type = db.Column(db.String(16))
    aka = db.Column(db.String(265))

    def url(self):
        return u"http://{0}:{1}/content/media/object_id/{0}/res_id/0".format(MEDIATOMB_SERVER_IP, MEDIATOMB_SERVER_PORT, self.mediatomb_id)


def find_media(filename):
    media = None

    conn = sqlite3.connect(MEDIATOMB_DATABASE_URI)
    cursor = conn.cursor()
    sql = """ select a.id, a.dc_title, a.mime_type, b.dc_title as aka from mt_cds_object as a
    left join mt_cds_object as b
    on a.parent_id = b.id
    where a.dc_title = ?"""
    cursor.execute(sql, (filename, ))
    row = cursor.fetchone()
    if not row is None:
        media = Media(row[0], row[1], row[2], row[3])
        #media = Media(row['id'], row['dc_title'], row['mime_type'], row['aka'])

    return media


def import_media(filename, encoding='utf-8'):
    for line in codecs.open(filename, 'r', encoding):
        line = line.rstrip()
        root, ext = os.path.splitext(line)
        if ext.lower() in MEDIA_EXTENSIONS:
            # get media filename
            h, t = os.path.split(line)
            media = find_media(t)
            if not media is None:
                db.session.add(media)

    db.session.commit()
