# Catálogo de fontes

O registro canônico é [config/sources.json](../config/sources.json). Esta página explica como preenchê-lo; não mantém uma segunda lista.

Cada entrada deve ter:

| Campo | Significado |
|---|---|
| `id` | Identificador estável, usado nas notas |
| `type` | document, meeting, message, calendar ou tasks |
| `purpose` | O que a fonte ajuda a resolver |
| `locator` | Caminho ou referência suficiente para encontrá-la, sem credenciais |
| `authority` | Assunto para o qual prevalece; conflitos que precisam de decisão |
| `authorized` | Permissão de uso confirmada para este escopo |
| `access_verified_at` | Data ISO da leitura real feita no ambiente de execução |
| `enabled` | Disponível para as rotinas; só habilitar após testar |
| `refresh` | Como conferir atualização e reconhecer uma cópia desatualizada |

Comece com `sources: []`. No cadastro, use um ID como `S01`; prefira referências estáveis em vez de cópias sem origem. O tipo de conta ou conexão disponível é verificado no aplicativo durante a aplicação. Se a leitura falhar, registre a limitação e não preencha a data de acesso como se tivesse funcionado.
