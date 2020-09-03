# -*- coding: utf-8 -*-
#
#  Matebot
#  
#  Copyleft 2012-2020 Iuri Guilherme <https://github.com/iuriguilherme>,
#     Matehackers <https://github.com/matehackers>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import datetime, locale, pytz

from matebot.ptb_matebot import (
  updaters,
)

from matebot.ptb_matebot.controllers.callbacks.jobqueue import (
  hourly_callback,
  daily_callback,
  its420_callback,
  script_start_callback,
)

def all():
  ### Job Queues
  here = pytz.timezone('America/Sao_Paulo')
  here_and_now = datetime.datetime.now(here)
  locale.setlocale(locale.LC_ALL, 'pt_BR')
  updaters[0].job_queue.run_repeating(
    hourly_callback,
    interval = datetime.timedelta(hours = 1),
    first = datetime.datetime(
      year = here_and_now.year,
      month = here_and_now.month,
      day = here_and_now.day,
      hour = here_and_now.hour,
      minute = 0,
      second = 0,
      microsecond = 0,
      tzinfo = here,
    ),
  )

  updaters[0].job_queue.run_repeating(
    daily_callback,
    interval = datetime.timedelta(days = 1),
    first = datetime.datetime(
      year = here_and_now.year,
      month = here_and_now.month,
      day = here_and_now.day,
      hour = 0,
      minute = 0,
      second = 0,
      microsecond = 0,
      tzinfo = here,
    ),
  )

  updaters[0].job_queue.run_repeating(
    its420_callback,
    interval = datetime.timedelta(days = 1),
    ## Hoje às 16:20
    first = datetime.datetime(
      year = here_and_now.year,
      month = here_and_now.month,
      day = here_and_now.day,
      hour = 16,
      minute = 20,
      second = 0,
      microsecond = 0,
      tzinfo = here,
    ),
  )

  ## run_once
  updaters[0].job_queue.run_once(
    script_start_callback,
    0,
  )
