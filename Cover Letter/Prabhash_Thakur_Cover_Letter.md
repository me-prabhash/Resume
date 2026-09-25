Prabhash Thakur
+91 8759480218 | thakurprabhash80@gmail.com | linkedin.com/in/imprabhash

[Date]

[Hiring Manager name, if you can find it — otherwise "Hiring Team"]
[Company]
[City]

Dear [Name / Hiring Team],

I'm applying for the Senior Data Engineer role at [Company]. I've spent the last eight years
building on Snowflake and dbt, and the last two doing something more specific: getting Gen AI
features into production on top of a warehouse that people already trust for reporting. That
second part is harder than it sounds, and it's the work I'd like to keep doing.

At KIPI.AI I lead a team of eight on a Data Mesh build for our largest client. Data products
across five domains, roughly 200 people using them. A fair bit of my time goes on the ordinary
parts of that job — sprint planning, reviewing other people's models, telling a stakeholder that
the thing they want will take three weeks and not three days. The rest goes on the pipelines.

Two projects are probably worth describing, because they're the ones I'd point to if you asked
what I actually do.

The first was a Q&A chatbot over documents nobody had been able to search: contracts, scanned
PDFs, DOCX files, and call recordings. I used AI_PARSE_DOCUMENT to get text out of them, chunked
and indexed it into Cortex Search, and wired Cortex COMPLETE in to generate answers. It shipped
as a Streamlit app inside Snowflake, so there was no new service to secure or host. Queries that
used to take someone an afternoon of digging now come back in seconds, and new joiners stopped
having to ask a colleague where things were.

The second was less glamorous and probably mattered more. A team was manually reading through
around 50,000 pieces of customer feedback a month — free-text survey responses, support emails,
call transcripts. I moved the classification and sentiment work into the enrichment pipeline with
CLASSIFY_TEXT, SENTIMENT and EXTRACT_ANSWER. A backlog that ran weeks became same-day output, and
three people went back to work they'd actually been hired for. Later I fine-tuned a model on the
client's own labelled data, which got classification accuracy up about 15% over the stock model.

I also care about the boring engineering underneath, because Gen AI features fall over quickly
without it. I've rewritten SCD2 logic and switched loads to micro-batching so a job could run on
an XS warehouse instead of an L. I've put dbt-expectations tests on models that had no coverage at
all and built a framework that alerts the domain owner when a rule breaks, rather than letting a
number quietly go wrong for a month. I've set up RBAC, row-level security and dynamic masking on
data where getting that wrong would have been a real problem.

On the modelling side I've used Data Vault, star schema and medallion, and I pick based on what
the client needs rather than what I used last time. Before KIPI I was at Beyond Key, Visual BI and
Tech Mahindra, mostly on Snowflake, dbt, Azure Data Factory and Power BI.

I hold SnowPro Advanced Architect, SnowPro Advanced Data Engineer, SnowPro Core, SnowPro Specialty:
Gen AI, and the dbt Developer certification. The certifications are a reasonable signal, but the
Data Mesh build taught me more than any of the exams did.

What I'm looking for is a team where the data platform is treated as a product rather than a
reporting layer, and where there's appetite to put AI features in front of users instead of
demoing them. If that's roughly what [Company] is doing, I'd like to talk.

Thanks for your time.

Prabhash Thakur
