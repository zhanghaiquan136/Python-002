
- 1. SELECT * FROM data;

```
funds = pd.read_csv(r'./funds.csv')
```

- 2. SELECT * FROM data LIMIT 10;

```
first_ten = funds.head(10)
```


- 3. SELECT id FROM data;  //id 是 data 表的特定一列

```
ids = funds['id']
```


- 4. SELECT COUNT(id) FROM data;

```
funds.id.count()
```

- 5. SELECT * FROM data WHERE id<1000 AND age>30;

```
funds[(funds.id < 50) & (funds.register_date > '2007-09-10')]
```

- 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;

```
funds.groupby('style').count()
```

- 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;

```
pd.merge(df1, df2, on='id')
```

- 8. SELECT * FROM table1 UNION SELECT * FROM table2;

```
pd.concat([df1, df2])
```

- 9. DELETE FROM table1 WHERE id=10;

```
funds.drop(11, axis=0)
```

- 10. ALTER TABLE table1 DROP COLUMN column_name;

```
funds.drop('name', axis=1)
```
