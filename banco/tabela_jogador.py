from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from database import Jogador, db_session, Time


def select_todos():
    # Buscar todos os times no banco
    # 1 - Montar o select
    # join(Tabela que eu quero juntar, condição = chave estrangeira igual chave primária)
    jogadores_sql = select(Jogador, Time).join(Time, Jogador.time_id == Time.id)
    # 2 - Executar o select
    # usar scalars quando tiver somente uma tabela
    jogadores = db_session.execute(jogadores_sql).all()

    return jogadores

def select_quantidade_total():
    jogadores_sql = select(func.count(Jogador.id))
    qtd_total = db_session.execute(jogadores_sql).scalar()
    return qtd_total

print(select_quantidade_total())

def salvar(nome, numero_camisa, posicao, time_id):
    try:
        # cria uma nova pessoa e adiciona na base de dados
        novos_times = Jogador(nome=nome, numero_camisa=int(numero_camisa), posicao=posicao, time_id=int(time_id))
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
