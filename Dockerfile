FROM python:3.7 AS DIST
WORKDIR /opt/barrier

COPY pyproject.toml pyproject.toml
COPY barrier barrier

RUN pip install poetry

RUN poetry build

# ----------------------------------------------------------------

FROM python:3.7 AS FINAL

WORKDIR /var/www

COPY --from=DIST /opt/barrier/dist /opt/barrier
RUN pip install /opt/barrier/barrier*.whl

ENV BARRIER_REDIRECT_URI ""
ENV BARRIER_USERINFO_URI ""
ENV BARRIER_ISSUER ""
ENV BARRIER_TOKEN_URI ""
ENV BARRIER_AUTH_URI ""
ENV BARRIER_CLIENT_SECRET ""
ENV BARRIER_CLIENT_ID ""
ENV BARRIER_SECRET_KEY ""

EXPOSE 8000/tcp

COPY entrypoint.sh .
CMD ./entrypoint.sh
