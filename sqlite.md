首先，确保已经安装了SQLite3。可以在命令行中输入sqlite3 --version来查看版本信息。如果没有安装，则需要根据不同的操作系统去官网下载并安装。

打开命令行或者终端，然后输入sqlite3命令来启动SQLite3交互式shell。这将会连接到默认的SQLite数据库文件（通常为当前目录下名为"main.db"的文件）。

若想连接其他数据库文件，可以使用.open <database_file>命令来指定要连接的数据库文件路径。比如 .open /path/to/mydatabase.db。

现在就可以在SQLite3 shell中执行SQL语句了。例如，创建表、插入数据等。以下是一些示例：

创建表： CREATE TABLE mytable (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);

插入数据： INSERT INTO mytable (name) VALUES ('John');

查询数据： SELECT * FROM mytable;

完成操作后，可以使用.exit命令退出SQLite3 shell。