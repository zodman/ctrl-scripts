# Control scripts applied to a database
Imagine this situation of creating a script to fix a database,
this script only will work  once, and then,  the system where was applied or the database. 

Now is  working fine.

Later you have same the situation again, you need to made another different script
that you are only going to apply it one time.

Then it becomes a list of scripts to run 1 time on something.

When you bring a backup, you have to apply all the scripts you already made on
the system/database to bring it up updated.

How do you keep track of the applied scripts ? 

```
ctrls add <file>
ctrls add-dir <path>
```


what about the status?

```
ctrls status <path>
```

This command will give you the actual status of the script if it was applied or dont.


Doing this It will create a table in the database called: `__ctrl_scripts_applied`


The database connection its taken from a variable environment or `.env` of

```
DATABASE_URL=
```

## For install

```
pip install https://github.com/zodman/ctrl-scripts/archive/refs/heads/main.zip
```
