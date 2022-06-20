<!--
Projeto de Recurso de Linguagens de Programação I 2021/22 (c) by Nuno Fachada
and Phil Lopes.

Projeto de Recurso de Linguagens de Programação I 2021/22 is licensed under a
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by-nc-sa/4.0/>.
-->

# Projeto de Recurso de Linguagens de Programação I 2021/22

## Introdução

Os grupos devem implementar uma simulação de pandemia na forma de uma aplicação
de consola .NET Core 3.1 na linguagem C#.

## Modelo para simulação

A simulação corre numa grelha _N x N_, na qual _M_ agentes se movem de forma
aleatória, sendo possível estar mais do que um agente na mesma posição. A
simulação funciona por turnos e em cada turno cada agente move-se
aleatoriamente uma posição na sua vizinhança de [Moore].

Um único agente, escolhido aleatoriamente, é infetado no turno
_T<sub>inf</sub>_. Um agente infetado morre e é removido da simulação após
_L_ turnos. No entanto enquanto está vivo e infetado, move-se normalmente,
infetando todos os agentes que se encontrem na mesma posição no fim de cada
turno.
Os novos infetados tornam-se imediatamente e igualmente contagiosos,
morrendo também ao fim de _L_ turnos.

A simulação termina após _T_ turnos ou quando todos os agentes morrerem
(aquilo que acontecer primeiro).

## Funcionamento da simulação

### Opções de linha de comando

O programa deve aceitar duas opções na linha de comando:

* `-N` - Uma das dimensões da grelha de simulação _N x N_.
* `-M` - Número de agentes inicialmente na simulação.
* `-L` - Tempo de vida de um agente (em turnos) após ter sido infetado.
* `-Tinf` - Turno em que ocorre a primeira infeção.
* `-T` - Número máximo de turnos.
* `-v` - Opção que ativa a visualização da simulação (ver próxima secção).
* `-o` - Opção que indica um ficheiro no qual serão gravadas as estatísticas
  da simulação em cada turno.

Um exemplo de execução:

```
dotnet run -- -N 50 -M 100 -L 10 -Tinf 5 -T 1000 -v -o stats.tsv
```

A primeira opção, `--`, serve para separar entre as opções do comando `dotnet`
e as opções do programa a ser executado, neste caso o nosso jogo.

As opções indicadas podem ser dadas em qualquer ordem. As opções `-N`, `-M`,
`-L`, `-Tinf` e `-T` são obrigatórias, e se alguma delas for omitida o programa
deve terminar com uma mensagem de erro indicando o modo de uso. A opção `-v` é
opcional, e a sua omissão leva a que a simulação corra sem visualização
(ver próxima secção). A opção `-o` também é opcional, e a sua omissão leva a
que o programa não grave as estatísticas da simulação num ficheiro.

Para quem preferir usar o Visual Studio Community 2019, as opções de linha de
comandos podem ser definidas diretamente da seguinte forma: 1) clicar com
o botão direito em cima do nome do projeto; 2) selecionar "Properties"; 3)
selecionar separador "Debug"; e, 4) na
caixa "Command line arguments" especificar os argumentos desejados.

### Visualização

Caso a opção `-v` seja omitida, o programa deve simplesmente imprimir algo
semelhante ao seguinte:

```
Simulation starts with 300 healthy agents.
Turn 1 done (300 healthy, 0 infected, 0 deceased)
Turn 2 done (300 healthy, 0 infected, 0 deceased)
Turn 3 done (299 healthy, 1 infected, 0 deceased)
Turn 4 done (297 healthy, 3 infected, 0 deceased)
...
```

Caso a opção `-v` seja dada, além do número de agentes saudáveis, infetados e
mortos, deve também ser mostrada e atualizada a grelha de simulação após cada
turno. Esta visualização deve ser muito simples, e obedecer às seguintes
regras, da mais importante para a menos importante:

* Uma posição na qual tenha morrido um agente no último turno deve ter
  cor de fundo vermelha.
* Uma posição que contenha pelo menos um agente infetado deve ter
  cor de fundo amarela.
* Uma posição que contenha apenas agentes saudáveis deve ter cor de fundo
  verde.
* Uma posição sem agentes deve ter a cor de fundo da consola.

### Ficheiro com estatísticas

Caso a opção `-o` tenha sido indicada na linha de comandos, o programa deve
exportar os resultados da simulação para um ficheiro em formato [TSV]
(_tab-separated values_), no qual cada linha representa o número de agentes
saudáveis, infetados e mortos no fim de cada turno. Os valores devem estar
separados por _tabs_ (`\t`), sendo o nome do ficheiro dado após a opção `-o`.
Fica um exemplo simples do possível conteúdo do ficheiro após 10 turnos:

```
300	0	0
300	0	0
299	1	0
297	3	0
296	4	0
291	9	0
282	18	0
277	23	0
269	30	1
260	37	3
```

A evolução da simulação pode ser posteriormente visualizada usando o
[_script_ Python incluído neste repositório](scripts/plotstats.py)
(requer bibliotecas Matplotlib e NumPy), que
aceita como único argumento na linha de comandos o ficheiro gerado pela
simulação. A seguinte imagem mostra uma possível evolução da simulação com
os parâmetros _N = 50_, _M = 2000_, _L = 8_, _T<sub>inf</sub> = 1_ e _T = 100_:

![Resultado da simulação.](img/stats.png "TResultado da simulação.")

### Resumo

Resumindo, a simulação é executada de acordo com os seguintes passos:

1. Se número de agentes vivos > 0 e turno atual < _T_:
   1. Se turno atual == _T<sub>inf</sub>_, infetar um agente aleatoriamente.
   2. Para cada agente vivo: mover uma posição aleatoriamente.
   3. Para cada posição: se existir um agente infetado na posição atual,
      todos os agentes saudáveis nessa mesma posição também ficam infetados.
   4. Contar número de agentes saudáveis, infetados e mortos, eventualmente
      guardar esta informação para posteriormente exportar para um ficheiro.
   5. Mostrar estatísticas do turno atual e possivelmente atualizar
      visualização (caso tenha sido dada a opção `-v`).
   6. Voltar ao ponto 1.
2. Exportar dados para ficheiro caso tenha sido indicada a opção `-o`.

## Requisitos do código

### Organização e estrutura do código

O código deve estar obrigatoriamente implementado da seguinte forma:

* O projeto deve ser implementado usando programação por objetos. Mais
  especificamente:
  * Cada tipo (classe, _struct_, interface ou `enum`) deve representar um
    conceito da simulação e/ou da aplicação.
  * Cada tipo (classe, etc) deve ter apenas uma responsabilidade bem definida,
    seguindo o [_single responsibility principle_][SRP].
  * O uso de herança e interfaces será **muito** valorizado neste projeto, mas
    apenas se o seu uso fizer sentido no contexto em que é utilizado. O **não
    uso** de herança e interfaces será penalizado.
* O código deve seguir uma estrutura _Model-View-Controller_ (MVC), tal como
  discutido na semana 11 de aulas.
* Cada classe, _struct_, interface ou enumeração deve ser colocada num ficheiro
  com o mesmo nome. Por exemplo, uma classe chamada `Location` deve ser colocada
  no ficheiro `Location.cs`.

### Eficiência do código

Existem variadíssimas formas de implementar esta simulação corretamente.
Soluções mais eficientes (que executem a simulação mais rapidamente) serão
bonificadas na nota. Todas as otimizações implementadas devem ser mencionadas
no relatório.

### Requisitos de multi-plataforma

A aplicação deve funcionar em Windows, macOS e Linux. A melhor estratégia para
garantir que assim seja é testar o jogo em Linux (e.g., numa máquina virtual).
Algumas instruções incompatíveis com macOS e Linux são, por exemplo:

* [Console.Beep()](https://docs.microsoft.com/dotnet/api/system.console.beep)
* [Console.SetBufferSize()](https://docs.microsoft.com/dotnet/api/system.console.setbuffersize)
* [Console.SetWindowPosition()](https://docs.microsoft.com/dotnet/api/system.console.setwindowposition)
* [Console.SetWindowSize()](https://docs.microsoft.com/dotnet/api/system.console.setwindowsize)
* Entre outras.

As instruções que só funcionam em Windows têm a seguinte indicação na sua
documentação:

![The current operating system is not Windows.](img/notsupported.png "The current operating system is not Windows.")

## Objetivos e critério de avaliação

Este projeto tem os seguintes objetivos:

* **O1** - Programa deve funcionar como especificado. Atenção aos detalhes,
  pois é fácil desviarem-se das especificações caso não leiam o enunciado com
  atenção.
* **O2** - Projeto e código bem organizados, nomeadamente:
  * Código organizado segundo o indicado na secção
    [Requisitos do código](#requisitos-do-código).
  * Código devidamente comentado e indentado.
  * Inexistência de código "morto", que não faz nada, como por exemplo
    variáveis, propriedades ou métodos nunca usados.
  * Projeto compila e executa sem erros e/ou *warnings*.
* **O3** - Projeto adequadamente documentado com [comentários de documentação
  XML][XML].
* **O4** - Repositório Git deve refletir boa utilização do mesmo, nomeadamente:
  * Devem existir *commits* de todos os elementos do grupo, _commits_ esses
    com mensagens que sigam as melhores práticas para o efeito (como indicado
    [aqui](https://chris.beams.io/posts/git-commit/),
    [aqui](https://gist.github.com/robertpainsi/b632364184e70900af4ab688decf6f53),
    [aqui](https://github.com/erlang/otp/wiki/writing-good-commit-messages) e
    [aqui](https://stackoverflow.com/questions/2290016/git-commit-messages-50-72-formatting)).
  * Ficheiros binários não necessários, como por exemplo todos os que são
    criados nas pastas `bin` e `obj`, bem como os ficheiros de configuração
    do Visual Studio (na pasta `.vs` ou `.vscode`), não devem estar no
    repositório. Ou seja, devem ser ignorados ao nível do ficheiro
    `.gitignore`.
  * *Assets* binários necessários, como é o caso da imagem do diagrama UML,
    devem ser integrados no repositório em modo Git LFS.
* **O5** - Relatório em formato [Markdown] (ficheiro `README.md`),
  organizado da seguinte forma:
  * Título do projeto.
  * Autoria:
    * Nome dos autores (primeiro e último) e respetivos números de aluno.
    * Informação de quem fez o quê no projeto. Esta informação é
      **obrigatória** e deve refletir os *commits* feitos no Git.
    * Indicação do repositório Git utilizado. Esta indicação é
      opcional, pois podem preferir manter o repositório privado após a
      entrega.
  * Arquitetura da solução:
    * Descrição da solução, com breve explicação de como o código foi
      organizado, bem como dos algoritmos não triviais que tenham sido
      implementados.
    * Um diagrama UML de classes simples (i.e., sem indicação dos
      membros da classe) descrevendo a estrutura de classes.
  * Referências, incluindo trocas de ideias com colegas, código aberto
    reutilizado (e.g., do StackOverflow) e bibliotecas de terceiros
    utilizadas. Devem ser o mais detalhados possível.
  * **Nota:** o relatório deve ser simples e breve, com informação mínima e
    suficiente para que seja possível ter uma boa ideia do que foi feito.
    Atenção aos erros ortográficos e à correta formatação [Markdown], pois
    ambos serão tidos em conta na nota final.

O projeto tem um peso de 10 valores na nota final da disciplina e será avaliado
de forma qualitativa. Isto significa que todos os objetivos têm de ser
parcialmente ou totalmente cumpridos. A cada objetivo, O1 a O5, será atribuída
uma nota entre 0 e 1. A nota do projeto será dada pela seguinte fórmula:

*N = 10 x O1 x O2 x O3 x O4 x O5 x D*

Em que *D* corresponde à nota da discussão e percentagem equitativa de
realização do projeto, também entre 0 e 1. Isto significa que se os alunos
ignorarem completamente um dos objetivos, não tenham feito nada no projeto ou
não comparecerem na discussão, a nota final será zero.

## Entrega

O projeto deve ser entregue por **grupos de 1 a 3 alunos** via Moodle até às
23h de 3 de julho de 2022. Um (e apenas um) dos elementos do grupo deve ser
submeter um ficheiro `zip` com a solução completa, nomeadamente:

* Pasta escondida `.git` com o repositório Git local do projeto.
* Ficheiro da solução (`.sln`).
* Pasta do projeto, contendo os ficheiros `.cs` e o ficheiro do projeto
  (`.csproj`).
* Ficheiro `README.md` contendo o relatório do projeto em formato [Markdown].
* Ficheiro de imagem contendo o diagrama UML. Este ficheiro deve ser incluído
  no repositório em modo Git LFS.
* Outros ficheiros de configuração, como por exemplo `.gitignore` e
  `.gitattributes`.

Não serão avaliados projetos sem estes elementos e que não sejam entregues
através do Moodle.

## Honestidade académica

Nesta disciplina, espera-se que cada aluno siga os mais altos padrões de
honestidade académica. Isto significa que cada ideia que não seja do
aluno deve ser claramente indicada, com devida referência ao respectivo
autor. O não cumprimento desta regra constitui plágio.

O plágio inclui a utilização de ideias, código ou conjuntos de soluções
de outros alunos ou indivíduos, ou quaisquer outras fontes para além
dos textos de apoio à disciplina, sem dar o respectivo crédito a essas
fontes. Os alunos são encorajados a discutir os problemas com outros
alunos e devem mencionar essa discussão quando submetem os projetos.
Essa menção **não** influenciará a nota. Os alunos não deverão, no
entanto, copiar códigos, documentação e relatórios de outros alunos, ou dar os
seus próprios códigos, documentação e relatórios a outros em qualquer
circunstância. De facto, não devem sequer deixar códigos, documentação e
relatórios em computadores de uso partilhado, e muito menos usar
repositórios Git públicos (embora os mesmos possam ser tornados públicos
12h após a data limite de submissão).

Nesta disciplina, a desonestidade académica é considerada fraude, com
todas as consequências legais que daí advêm. Qualquer fraude terá como
consequência imediata a anulação dos projetos de todos os alunos envolvidos
(incluindo os que possibilitaram a ocorrência). Qualquer suspeita de
desonestidade académica será relatada aos órgãos superiores da escola
para possível instauração de um processo disciplinar. Este poderá
resultar em reprovação à disciplina, reprovação de ano ou mesmo suspensão
temporária ou definitiva da ULHT.

*Texto adaptado da disciplina de [Algoritmos e
Estruturas de Dados][aed] do [Instituto Superior Técnico][ist]*

## Referências

* Charbonneau, P. (2017). **Natural Complexity**. Princeton University
  Press.
* Whitaker, R. B. (2016). **The C# Player's Guide** (3rd Edition).
  Starbound Software.
* Albahari, J. (2017). **C# 7.0 in a Nutshell**. O’Reilly Media.
* Dorsey, T. (2017). **Doing Visual Studio and .NET Code Documentation
  Right**. Visual Studio Magazine. Retrieved from
  <https://visualstudiomagazine.com/articles/2017/02/21/vs-dotnet-code-documentation-tools-roundup.aspx>.

## Licenças

* Este enunciado é disponibilizado através da licença [CC BY-NC-SA 4.0].

## Metadados

* Autores: [Nuno Fachada] e [Phil Lopes]
* Curso:  [Licenciatura em Videojogos][lamv]
* Instituição: [Universidade Lusófona de Humanidades e Tecnologias][ULHT]

[CC BY-NC-SA 4.0]:https://creativecommons.org/licenses/by-nc-sa/4.0/
[lamv]:https://www.ulusofona.pt/licenciatura/videojogos
[Phil Lopes]:https://github.com/worshipcookies
[Nuno Fachada]:https://github.com/fakenmc
[ULHT]:https://www.ulusofona.pt/
[aed]:https://fenix.tecnico.ulisboa.pt/disciplinas/AED-2/2009-2010/2-semestre/honestidade-academica
[ist]:https://tecnico.ulisboa.pt/pt/
[Markdown]:https://guides.github.com/features/mastering-markdown/
[Doxygen]:https://www.stack.nl/~dimitri/doxygen/
[DocFX]:https://dotnet.github.io/docfx/
[KISS]:https://en.wikipedia.org/wiki/KISS_principle
[XML]:https://docs.microsoft.com/dotnet/csharp/codedoc
[SRP]:https://en.wikipedia.org/wiki/Single_responsibility_principle
[2º projeto de LP1 2018/19]:https://github.com/VideojogosLusofona/lp1_2018_p2_solucao
[Moore]:https://en.wikipedia.org/wiki/Moore_neighborhood
[TSV]:https://en.wikipedia.org/wiki/Tab-separated_values