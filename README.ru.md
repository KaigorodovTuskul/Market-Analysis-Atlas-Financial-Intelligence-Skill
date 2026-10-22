# Market Analysis Atlas — скилл по анализу финансовых рынков

Самостоятельная база знаний и Agent Skill для **технического, фундаментального, макроэкономического, долгового, количественного и криптовалютного анализа**. Оформлен по принципу [`pareto-forge`](https://github.com/KaigorodovTuskul/pareto-forge): компактный `SKILL.md`, подключаемые тематические справочники, воспроизводимые скрипты и тесты.

## Что находится в архиве

| Компонент | Состояние |
|---|---:|
| Оригинальные определения | **533** (на английском языке, 10 категорий) |
| Схемы графических и свечных паттернов | **100** оригинальных SVG |
| Формулы, методические оговорки, типичные ошибки | Да |
| Поиск по словарю из CLI | Да, без сторонних зависимостей |
| Установщик для Codex / OpenCode / Claude Code / Cursor | Да |
| Автоматическая выгрузка всех статей Investopedia | **Нет** — тексты/графика не скопированы |
| Дополнительный каталог названий и URL | Опциональный инструмент, не запускался; соблюдает `robots.txt` |

**Объем не равен полному словарю Investopedia.** По данным самого сайта, он включает порядка 14 тысяч словарных определений, в том числе юридические, страховые, налоговые и бытовые финансовые понятия. В базу включены 533 специально написанные карточки по темам анализа финансовых рынков, а не все статьи. Это существенное ограничение, отраженное в [отчете о покрытии](docs/COVERAGE.md).

## Установка

Опубликуйте содержимое ZIP как отдельный GitHub-репозиторий и используйте:

```bash
npx skills add KaigorodovTuskul/Market-Analysis-Atlas-Financial-Intelligence-Skill --skill market-analysis-atlas
```

Или установите локально из распакованного репозитория:

```bash
python scripts/install.py --project /path/to/project --agent codex
python scripts/install.py --project /path/to/project --agent opencode
python scripts/install.py --project /path/to/project --agent claude-code
```

## Публикация и релизы

Репозиторий состоит из обычных файлов и stdlib Python — отдельной сборки или сервера нет. Первая публикация:

```bash
git init
git add .
git commit -m "Release 1.0.0"
git branch -M main
git remote add origin https://github.com/KaigorodovTuskul/Market-Analysis-Atlas-Financial-Intelligence-Skill.git
git push -u origin main

# Опционально: тег и GitHub Release
git tag -a v1.0.0 -m "Market Analysis Atlas 1.0.0"
git push origin v1.0.0
```

Архив для распространения: `python scripts/package.py --output dist/market-analysis-atlas.zip`. Файл `RELEASE_MANIFEST.json` фиксирует версию, счетчики и SHA-256 трех основных data-файлов для проверки происхождения релиза; в рантайме он не используется. CI в `.github/workflows/ci.yml` запускает валидацию и тесты при каждом push и pull request.

## Примеры

```bash
python scripts/atlas.py "head and shoulders" --detail
python scripts/atlas.py "yield curve" --limit 20
python scripts/atlas.py --category macro --limit 150
python scripts/atlas.py --stats
python scripts/validate.py
python -m unittest discover -s tests -v
```

Графики — **схемы на искусственных данных**. Они не скачаны с Investopedia и не доказывают, что паттерн приносит прибыль. Политика источников, проверка гипотез, учет статистической неопределенности, корректировка на расходы и риск включены в инструкции скилла.

## Расширение словаря

`python scripts/sync_index.py --allow-site-fetch` — инструмент для сбора **только названий и URL** с разрешенных страниц алфавитного каталога. Перед запуском необходимо самостоятельно проверить актуальные правила сайта; скрипт не обходит запреты и не скачивает описания или изображения. Заполнить весь корпус авторскими статьями можно отдельно с юридически допустимыми источниками и редакторской проверкой.

См. также [английскую документацию](README.md), [правила работы с источниками](docs/METHODOLOGY.md) и [ограничения](docs/COVERAGE.md).
