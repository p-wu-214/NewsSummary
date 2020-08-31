select a.article_id, a.content from articles a
left join summaries s on s.article_id = a.article_id
where s.article_id is null
order by article_id