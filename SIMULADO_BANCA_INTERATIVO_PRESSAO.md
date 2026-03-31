# Simulado de Banca Interativo — Treino sob Pressão

Objetivo: treinar sua capacidade de responder com clareza quando a banca interrompe, pressiona e tenta expor contradições.

Como usar:
- Faça em voz alta.
- Um colega (ou você mesmo lendo em voz diferente) faz o papel da banca.
- Tempo por resposta principal: 60 a 90 segundos.
- Tempo por contra-pergunta: 20 a 40 segundos.

Regra de ouro:
- Não entre em defensiva.
- Não invente o que não está no código.
- Use estrutura: contexto → decisão → trade-off → próximo passo.

---

## Bloco 1 — Abertura sob pressão

## Cenário A: "Seu projeto está simples demais"

**Banca:** "Isso aí não é arquitetura de verdade, é só CRUD com tela bonita. O que tem de engenharia aqui?"

**Resposta modelo (forte):**
"A engenharia está nas decisões de separação de domínio, contratos entre serviços, autenticação distribuída e composição de microfrontend. Eu não otimizei por complexidade, otimizei por entrega confiável do fluxo central dentro do prazo. O PMV roda com serviços independentes, bancos isolados, CI e fallback para componentes externos como IA e cache."

**Interrupção 1:** "Separar em dois serviços não foi exagero?"
- **Resposta curta:** "Não, porque users/auth e pedidos têm ciclos de evolução diferentes e isolamento evita acoplamento futuro."

**Interrupção 2:** "Cadê valor disso hoje?"
- **Resposta curta:** "Valor imediato: responsabilidades claras, deploy e manutenção independentes, e risco reduzido de mudanças em auth afetarem pedidos."

---

## Bloco 2 — Segurança (perguntas agressivas)

## Cenário B: "Seu auth é fraco"

**Banca:** "Token em localStorage? CORS aberto? Isso não passaria em produção séria."

**Resposta modelo (honesta e madura):**
"Concordo para cenário internet/publico. Aqui a escolha foi de PMV interno com foco em fluxo funcional em prazo curto. Eu reconheço os riscos: exposição a XSS para token e permissividade de origem. A evolução planejada é endurecer CORS por domínio, revisar estratégia de sessão e adicionar política de autorização mais granular."

**Interrupção 1:** "Então você sabia que estava inseguro e entregou assim mesmo?"
- **Resposta curta:** "Sabia dos limites e documentei o risco. A decisão foi consciente de prioridade, não desconhecimento técnico."

**Interrupção 2:** "Por que não implementou refresh token?"
- **Resposta curta:** "Pelo custo-benefício no prazo. Primeiro garanti autenticação estável e fluxo principal; refresh entra como evolução natural."

---

## Bloco 3 — Arquitetura e trade-offs

## Cenário C: "Por que FastAPI e não Django?"

**Banca:** "Você escolheu FastAPI por modismo?"

**Resposta modelo:**
"Não. Para este recorte, FastAPI reduziu boilerplate, trouxe validação forte com Pydantic e documentação automática dos endpoints. Isso acelerou entrega sem sacrificar legibilidade. Django REST também resolveria, mas com maior custo de setup para o PMV proposto."

**Interrupção 1:** "Então Django seria pior?"
- **Resposta curta:** "Não é pior, é outra curva de custo-benefício para esse prazo e escopo."

**Interrupção 2:** "Você faria a mesma escolha em sistema maior?"
- **Resposta curta:** "Depende do contexto de time/domínio. Em sistema maior, pesaria ecossistema, maturidade da equipe e padrões já adotados."

---

## Bloco 4 — Perguntas para te desestabilizar

## Cenário D: "Prove que entende, sem decorar"

**Banca:** "Explica agora, sem enrolar: como o token nasce, por onde passa e onde é validado?"

**Resposta modelo:**
"No login, o users-service recebe credenciais, valida senha hash e emite JWT com claims básicas e expiração. O frontend armazena e envia no header Authorization Bearer. O orders-service valida localmente a assinatura com o mesmo segredo e usa o payload para autorização nos endpoints protegidos."

**Contra-pergunta:** "Qual endpoint de pedidos exige token obrigatório?"
- **Resposta curta:** "Atualização de status via PATCH de pedido."

**Contra-pergunta:** "O que acontece sem token?"
- **Resposta curta:** "Retorna 401 no endpoint protegido."

---

## Bloco 5 — Infra e operação

## Cenário E: "Seu sistema cai fácil"

**Banca:** "Derrubo um serviço e acabou tudo."

**Resposta modelo:**
"Não necessariamente. A própria demonstração de resiliência mostra isso: com users-service fora, o módulo de pedidos ainda consegue leitura em endpoints que não exigem auth obrigatória. O impacto aparece nas operações protegidas, que retornam 401."

**Interrupção 1:** "Isso é gambiarra, não resiliência."
- **Resposta curta:** "É degradação controlada para PMV. Resiliência madura incluiria circuit breaker e observabilidade completa, que são próximos passos."

**Interrupção 2:** "Cadê fila para desacoplamento?"
- **Resposta curta:** "Não implementei fila por priorização de escopo. Foquei no fluxo principal estável e testado."

---

## Bloco 6 — IA sob questionamento duro

## Cenário F: "IA é enfeite"

**Banca:** "Se tirar IA, seu sistema muda o quê?"

**Resposta modelo:**
"A IA neste projeto é componente de enriquecimento, não núcleo transacional. Ela agrega classificação de prioridade e resumo operacional. O sistema foi desenhado para continuar funcional sem IA, com fallback previsível, justamente para não tornar serviço externo um ponto único de falha."

**Interrupção 1:** "Então por que colocou IA?"
- **Resposta curta:** "Para demonstrar integração prática com valor de negócio sem comprometer robustez do fluxo principal."

**Interrupção 2:** "Como evita saída inválida do modelo?"
- **Resposta curta:** "Normalização de prioridade e fallback padrão em erro de parsing/chamada."

---

## Bloco 7 — Testes e qualidade

## Cenário G: "Seu teste não prova nada"

**Banca:** "Mockou tudo no orders. Isso mascara problema real."

**Resposta modelo:**
"Mocks foram usados para dependências externas instáveis (cache e IA), buscando determinismo na CI. Ainda assim, os contratos principais de endpoint e regras de API estão validados. Concordo que a próxima evolução é teste de integração com infraestrutura real para cobrir comportamento distribuído."

**Interrupção 1:** "Por que não fez isso já?"
- **Resposta curta:** "Priorização de entregáveis obrigatórios no prazo."

**Interrupção 2:** "Qual teste faltante você faria primeiro?"
- **Resposta curta:** "Integração ponta a ponta de criação e atualização de pedido com PostgreSQL e autenticação real."

---

## Bloco 8 — Produto e priorização

## Cenário H: "Você escolheu errado o que fazer"

**Banca:** "Você investiu em IA, mas faltou observabilidade. Má priorização, não?"

**Resposta modelo:**
"É uma crítica válida dependendo do objetivo. Aqui havia também objetivo de demonstrar capacidade técnica de integração. Ainda assim, não deixei o core vulnerável: IA é opcional com fallback. Se o foco fosse produção imediata, eu inverteria a ordem e priorizaria observabilidade antes de IA."

**Interrupção 1:** "Então você faria diferente hoje?"
- **Resposta curta:** "Para produção, sim: observabilidade e segurança primeiro. Para desafio técnico, a decisão foi equilibrada."

---

## Bloco 9 — Rodadas relâmpago (30 segundos cada)

1. Onde está o maior risco técnico hoje?
2. Qual endpoint você protegeria adicionalmente primeiro?
3. O que quebra se Redis ficar fora?
4. Qual seu plano de evolução em 30 dias?
5. Como você reduziria acoplamento frontend-backend?
6. Qual trade-off mais importante você tomou?
7. Qual evidência concreta de qualidade você apresenta?
8. Qual decisão você defenderia mesmo sob crítica?
9. O que você removeria para simplificar ainda mais?
10. O que você adicionaria para produção amanhã?

---

## Bloco 10 — Simulação completa de 20 minutos (roteiro)

## Minuto 0–2: abertura
- Contexto do problema.
- Objetivo do PMV.

## Minuto 2–7: arquitetura
- Serviços e responsabilidade.
- Fluxo de autenticação.
- Composição dos MFEs.

## Minuto 7–13: demo
- Login.
- Lista e filtro.
- Criação.
- Atualização de status.
- Resiliência.

## Minuto 13–17: decisões técnicas
- FastAPI, JWT compartilhado, Redis cache, IA opcional.
- Trade-offs e limites reconhecidos.

## Minuto 17–20: próximos passos
- Segurança, observabilidade, integração avançada, testes de integração.

---

## Kit de respostas prontas (frases de ancoragem)

Use estas frases quando travar:

- "Ótimo ponto; no estado atual eu tratei isso como trade-off de PMV."
- "No código hoje, o comportamento é este; a evolução planejada é esta."
- "Escolhi reduzir risco de entrega primeiro, e complexidade operacional depois."
- "Eu não implementei esse item, e a justificativa técnica foi prioridade de fluxo central no prazo."
- "Se o recorte fosse produção imediata, eu priorizaria segurança/observabilidade antes de expansão funcional."

---

## Anti-padrões na banca (evite)

- Inventar feature que não existe no código.
- Dizer "não sei" sem completar com plano de investigação.
- Entrar em discussão emocional com avaliador.
- Defender decisão sem mencionar trade-off.
- Resposta longa sem objetividade.

---

## Modelo de resposta quando você não sabe

"Não tenho esse número exato agora. O que eu consigo afirmar pelo código é [fato verificável]. Para fechar com precisão, eu validaria [método objetivo] e retornaria com [resultado esperado]."

Isso mostra maturidade, honestidade e método.

---

## Plano de treino em 3 dias

## Dia 1
- Blocos 1 a 4 (fundamentos e segurança).
- Grave áudio e avalie clareza.

## Dia 2
- Blocos 5 a 8 (resiliência, IA, testes, priorização).
- Treine resposta curta vs aprofundada.

## Dia 3
- Simulação completa de 20 minutos + rodadas relâmpago.
- Objetivo: consistência sem contradição com o código.

---

## Critério de pronto

Você está pronto quando:
- Responde firme sem inventar.
- Assume limites sem parecer fraco.
- Conecta decisão técnica a contexto de prazo e valor.
- Mantém postura calma sob interrupção.

Se quiser, próximo passo eu monto uma versão "cartão de bolso" (1 página) com apenas gatilhos de resposta para levar aberto durante o ensaio.