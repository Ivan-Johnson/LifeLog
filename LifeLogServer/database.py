#This file is a fork of sample code from the Flask project, available here:
#https://web.archive.org/web/20200101161533/https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
#
#As per https://web.archive.org/web/20200101161535/https://flask.palletsprojects.com/en/1.1.x/license/
#that file is available under this license:
#
#Copyright 2010 Pallets
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#1: Redistributions of source code must retain the above copyright notice, this
#list of conditions and the following disclaimer.
#
#2: Redistributions in binary form must reproduce the above copyright notice,
#this list of conditions and the following disclaimer in the documentation
#and/or other materials provided with the distribution.
#
#3: Neither the name of the copyright holder nor the names of its contributors
#may be used to endorse or promote products derived from this software without
#specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sqlite3

import click
import flask as f
import functools

from http import HTTPStatus

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in f.g:
        f.g.db = sqlite3.connect(
            f.current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        f.g.db.row_factory = sqlite3.Row

    return f.g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = f.g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with f.current_app.open_resource("schema.sql") as file:
        db.executescript(file.read().decode("utf8"))

def get_autocommit_db(func=None, /):
    AUTH_HEADER="token"
    if not func:
        return functools.partial(get_autocommit_db)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)

        status_code = None
        if isinstance(response, tuple):
            (_, status_code) = response
        elif isinstance(response, f.Response):
            status_code = response.status_code
        else:
            assert False, "Unrecognized response from function decorated by get_autocommit_db"

        if status_code == HTTPStatus.OK:
            db = get_db()
            db.commit()

        return response
    return wrapper



@click.command("init-db")
@f.cli.with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
