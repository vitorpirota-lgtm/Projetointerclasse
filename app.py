from os import times

from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from banco import tabela_time, tabela_jogador, tabela_partida
from database import *

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():

    times = tabela_time.select_quantidade_total()

    jogadores = tabela_jogador.select_quantidade_total()

    partidas = tabela_partida.select_quantidade_total()


    return render_template(
        "dashboard.html",
        total_jogadores=jogadores,
        total_times=times,
        total_partidas=partidas,
    )


@app.route("/jogadores")
def listar_jogadores():
    jogadores = tabela_jogador.select_todos()
    return render_template("jogadores.html", jogadores=jogadores)

@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None

        # Verifica se foi digitado
        if not nome:
            flash('Preencha o nome do jogador', 'error')
            return render_template('jogadores.html')
        if not numero_camisa:
            flash('Preencha o numero da camisa', 'error')
            return render_template('jogadores.html')
        if not posicao:
            flash('Preencha a posicao', 'error')
            return render_template('jogadores.html')
        if not time_id:
            flash('Preencha o time', 'error')
            return render_template('jogadores.html')

        # SALVAR NO BANCO DE DADOS:
        tabela_jogador.salvar(nome=nome, numero_camisa=int(numero_camisa), posicao=posicao, time_id=int(time_id))

        return redirect(url_for("listar_jogadores"))


    jogadores = tabela_jogador.select_todos()
    print(jogadores)


    times = tabela_time.select_todos()
    print(times)
    return render_template("jogadores.html", jogadores=jogadores, times=times)

@app.route("/jogadores/excluir/<jogador_id>", methods=[ "GET", "POST"])
def excluir_jogador(jogador_id):
    print(jogador_id)
    jogador_sql = select(Jogador).where(Jogador.id == jogador_id)
    jogador = db_session.execute(jogador_sql).scalar_one_or_none()
    if jogador:

        db_session.delete(jogador)
        db_session.commit()
    return redirect(url_for('listar_jogadores'))


@app.route("/times")
def listar_times():
    times = tabela_time.select_todos()
    return render_template("times.html", times=times)


@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()  # strip corta os comentários!
        turma = request.form.get("turma", "").strip()
        responsavel = request.form.get("responsavel", "").strip()
        # Verificar se foi digitado
        if not nome:
            flash('Preencha o nome do time', 'error')
            return render_template('times.html')
        if not turma:
            flash('Preencha a turma', 'error')
            return render_template('times.html')
        if not responsavel:
            flash('Preencha o nome do responsavel', 'error')
            return render_template('times.html')

        # SALVAR NO BANCO:
        tabela_time.salvar(nome=nome, turma=turma, responsavel=responsavel)

        times = tabela_time.select_todos()
        return render_template("times.html", times=times)

    times = tabela_time.select_todos()
    print(times)
    return render_template("times.html", times=times)

@app.route("/times/excluir/<time_id>", methods=[ "GET", "POST"])
def excluir_time(time_id):
    print(time_id)
    time_sql = select(Time).where(Time.id == time_id)
    time = db_session.execute(time_sql).scalar_one_or_none()
    if time:

        db_session.delete(time)
        db_session.commit()
    return redirect(url_for('listar_times'))



@app.route("/partidas")
def listar_partidas():
    partidas = tabela_partida.select_todos()
    return render_template("partidas.html", partidas=partidas)


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():
    if request.method == "POST":
        # Pegar os campos do formulário
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()

        # Verificar se foi digitado
        if not time_casa_id:
            flash('Preencha o nome do time', 'error')
            return redirect(url_for('nova_partida'))
        if not time_visitante_id:
            flash('Preencha o nome do time', 'error')
            return redirect(url_for('nova_partida'))
        if not gols_casa:
            flash('Preencha o numero de gols', 'error')
            return redirect(url_for('nova_partida'))
        if not gols_visitante:
            flash('Preencha o numero de gols', 'error')
            return redirect(url_for('nova_partida'))
        if not data_partida:
            flash('Preencha a data da partida', 'error')
            return redirect(url_for('nova_partida'))

        # Verificar se os times são iguais
        if time_casa_id == time_visitante_id:
            flash('Os times não podem ser iguais', 'error')
            return redirect(url_for('nova_partida'))

        # SALVAR NO BANCO
        tabela_partida.salvar(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)

    partidas = tabela_partida.select_todos()
    times = tabela_time.select_todos()
    return render_template("partidas.html",  partidas=partidas, times=times)


@app.route("/partidas/excluir/<partida_id>", methods=[ "GET", "POST"])
def excluir_partida(partida_id):
    print(partida_id)
    partida_sql = select(Partida).where(Partida.id == partida_id)
    partida = db_session.execute(partida_sql).scalar_one_or_none()
    if partida:

        db_session.delete(partida)
        db_session.commit()
    return redirect(url_for('listar_partidas'))






if __name__ == "__main__":
    app.run(debug=True)
