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
        # Lançar o navegador
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.set_default_timeout(120000) # 2 minutos de fôlego para o robô

        print("Abrindo página de login do Duolingo...")
        page.goto("https://www.duolingo.com/log-in")

        # Verificar se precisa logar
        if "learn" not in page.url:
            print("Iniciando processo de login...")
            try:
                # Espera o campo de e-mail aparecer
                print("Preenchendo dados...")
                page.wait_for_selector('data-test=email-input', timeout=30000)
                page.fill('data-test=email-input', username)
                page.fill('data-test=password-input', password)
                
                # Tenta vários seletores para o botão de entrar
                print("Clicando no botão de entrar...")
                selectors = ['data-test=login-button', 'data-test=register-button', 'button:has-text("Entrar")', 'button:has-text("Login")']
                clicked = False
                for sel in selectors:
                    btn = page.locator(sel)
                    if btn.is_visible():
                        btn.click()
                        clicked = True
                        break
                
                if not clicked:
                    page.keyboard.press("Enter")

                # Esperar o redirecionamento
                print("Aguardando carregar a página principal (isto pode demorar)...")
                try:
                    page.wait_for_url("**/learn*", timeout=60000)
                    print("Login realizado com sucesso!")
                except Exception:
                    print(f"Aviso: Não chegou em /learn. URL atual: {page.url}")
                    # Verificar se tem mensagem de erro visível
                    if page.locator('text="incorrect"').is_visible() or page.locator('text="incorreta"').is_visible():
                        print("🚨 ERRO: Senha ou E-mail incorretos!")
                    elif page.locator('text="captcha"').is_visible() or page.locator('canvas').is_visible():
                        print("🚨 ERRO: O Duolingo pediu um CAPTCHA (desafio humano).")
                    else:
                        print("Página atual parece diferente. Tentando seguir mesmo assim...")
                        # Se já estivermos logados mas em outra página, o código abaixo pode funcionar
            except Exception as e:
                print(f"Erro no login: {e}")
                print(f"URL na hora do erro: {page.url}")
                page.screenshot(path="debug_login_error.png")
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
