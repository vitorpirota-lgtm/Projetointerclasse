from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from database import Time, db_session, Jogador


def select_todos():
    # Buscar todos os times no banco
    # 1 - Montar o select
    times_sql = (
        select(Time, func.count(Jogador.id).label('jogadores'))
        .outerjoin(Jogador, Jogador.time_id == Time.id)
        .group_by(Time.id)
    )
    # 2 - Executar o select
    times = db_session.execute(times_sql).all()

    return times

def select_quantidade_total():
    times_sql = select(func.count(Time.id))
    qtd_total = db_session.execute(times_sql).scalar()
    return qtd_total

print(select_quantidade_total())

def salvar(nome, turma, responsavel):
    try:
        # cria uma nova pessoa e adiciona na base de dados
        novos_times = Time(nome=nome, turma=turma, responsavel=responsavel)
        # Inicializa a sessão do banco de dados
        db_session.add(novos_times)
        db_session.commit()
        flash("Time criado com sucesso", category='success')
        print(f'{novos_times}')
    except SQLAlchemyError as e:
        db_session.rollback()  # Reverte a transação em caso de erro
        print(f'Erro ao salvar time no banco: {e}')
        flash('Erro ao salvar time no banco', category='error')
    except Exception as e:
        db_session.rollback()
        print(f'Erro inesperado', e)
        flash('Erro, tente novamente', category='error')
