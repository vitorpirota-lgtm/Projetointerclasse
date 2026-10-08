import time
from operator import or_

from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased

from database import Partida, db_session, Time


def select_todos():
    # Buscar todos os times no banco
    # 1 - Montar o select

    TimeCasa = aliased(Time)
    TimeVisitante = aliased(Time)

    partidas_sql = (
        select(Partida, TimeCasa, TimeVisitante)
        .join(TimeCasa, Partida.time_casa_id == TimeCasa.id)
        .join(TimeVisitante, Partida.time_visitante_id == TimeVisitante.id)
    )


    # 2 - Executar o select
    partidas_casa = db_session.execute(partidas_sql).all()
    return partidas_casa

def select_quantidade_total():
    partidas_sql = select(func.count(Partida.id))
    qtd_total = db_session.execute(partidas_sql).scalar()
    return qtd_total

print(select_quantidade_total())

def salvar(time_casa_id, time_visitante_id, gols_casa, gols_visitante, data_partida):
    try:
        # cria uma nova pessoa e adiciona na base de dados
        novas_partidas = Partida(time_casa_id=int(time_casa_id), time_visitante_id=int(time_visitante_id), gols_casa=int(gols_casa), gols_visitante=int(gols_visitante), data_partida=data_partida)
        # Inicializa a sessão do banco de dados
        db_session.add(novas_partidas)
        db_session.commit()
        flash("Time criado com sucesso", category='success')
        print(f'{novas_partidas}')
    except SQLAlchemyError as e:
        db_session.rollback()  # Reverte a transação em caso de erro
        print(f'Erro ao salvar time no banco: {e}')
        flash('Erro ao salvar time no banco', category='error')
    except Exception as e:
        db_session.rollback()
        print(f'Erro inesperado', e)
        flash('Erro, tente novamente', category='error')