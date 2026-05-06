import os
import time
from playwright.sync_api import sync_playwright

def run_streak():
    username = os.getenv("DUO_USERNAME")
    password = os.getenv("DUO_PASSWORD")

    if not username or not password:
        print("Erro: DUO_USERNAME ou DUO_PASSWORD não configurados nos Secrets do GitHub.")
        return

    with sync_playwright() as p:
        # Lançar o navegador (headless=True para rodar no GitHub Actions)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print("Abrindo Duolingo...")
        page.goto("https://www.duolingo.com/?is_login=true")

        # Verificar se precisa logar
        if "learn" not in page.url:
            print("Fazendo login...")
            try:
                # Clica no botão de login se existir
                login_btn = page.locator('data-test=have-account')
                if login_btn.is_visible():
                    login_btn.click()
                
                page.fill('data-test=email-input', username)
                page.fill('data-test=password-input', password)
                
                # Tenta o botão de login (pode ser login-button ou register-button dependendo da versão)
                login_submit = page.locator('data-test=login-button')
                if not login_submit.is_visible():
                    login_submit = page.locator('data-test=register-button')
                
                login_submit.click()
                print("Botão de entrar clicado, aguardando redirecionamento...")
                
                # Esperar um pouco mais e ver se aparece erro de senha
                time.sleep(5)
                if page.locator('text="Senha incorreta"').is_visible() or page.locator('text="usuário não encontrado"').is_visible():
                    print("Erro: Usuário ou senha incorretos no Duolingo!")
                    page.screenshot(path="login_fail_credentials.png")
                    browser.close()
                    return

                page.wait_for_url("**/learn*", timeout=45000)
                print("Login realizado com sucesso!")
            except Exception as e:
                print(f"Erro ao logar: {e}")
                # Tirar screenshot para debug se der erro
                page.screenshot(path="login_error.png")
                browser.close()
                return

        # Ir para uma lição de prática (Escuta é a mais fácil de pular)
        print("Iniciando lição de prática...")
        page.goto("https://www.duolingo.com/practice/listening")
        time.sleep(5)

        # Loop para completar a lição (puxando o seu código original de 11 tarefas)
        for i in range(1, 15): # Um pouco mais de margem
            print(f"Tarefa {i}...")
            try:
                # Esperar o botão de Pular ou Verificar aparecer
                # Duolingo usa data-test para os botões principais
                skip_btn = page.locator('data-test=player-skip')
                next_btn = page.locator('data-test=player-next')
                continue_btn = page.locator('data-test=player-continue')

                if skip_btn.is_visible(timeout=5000):
                    skip_btn.click()
                    print("  Pulei")
                elif next_btn.is_visible(timeout=5000):
                    next_btn.click()
                    print("  Verifiquei")
                elif continue_btn.is_visible(timeout=5000):
                    continue_btn.click()
                    print("  Continuei")
                
                time.sleep(2)
                
                # Se o botão de continuar aparecer após verificar
                if continue_btn.is_visible(timeout=2000):
                    continue_btn.click()
                    print("  Continuei (pós-verificação)")

            except Exception as e:
                print(f"Aviso na tarefa {i}: {e}")
                if "learn" in page.url:
                    print("Parece que a lição acabou ou voltamos para o menu.")
                    break

        print("Ofensiva Mantida!! Encerrando Programa!!")
        page.screenshot(path="final_state.png")
        browser.close()

if __name__ == "__main__":
    run_streak()
