FROM python:3.11-bullseye as python-base
LABEL authors="Juxan"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base as builder-base
RUN apt-get update


WORKDIR $PYSETUP_PATH
COPY ./pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir setuptools wheel \
 && pip install --no-cache-dir poetry

RUN poetry install --no-dev

FROM python-base as production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

WORKDIR code_root/

COPY src /code_root/src
COPY config.ini config.ini
COPY locales locales

#CMD ["ls", "-lsa"]
ENV PYTHONPATH "${PYTHONPATH}:/code_root/src"

#CMD ["python", "src/polite_bot.py"]
CMD python -u src/polite_bot.py
#ENTRYPOINT ["", "-b"]