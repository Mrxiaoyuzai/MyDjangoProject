# Database
#'ENGINE': 'django.db.backends.sqlite3',
 #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
   'default': {      
         'ENGINE': 'sql_server.pyodbc', #数据库引擎设置
         'NAME': 'OverDueRemind',#要连接的数据库名
       
         'USER': 'sa', #数据库用户名
       
         'PASSWORD': '1qaz2wsx', #数据库密码
     
         'HOST': '10.79.24.64',   #数据库主机地址
        
         'PORT': '',#数据库端口号，默认可以不写
      
          'OPTIONS': {
              'driver':'SQL Server Native Client 10.0',  #选项，这个要先在操作系统上完成ODBC的连接创建，并连接成功，注意10.0这个地方，要和自己的ODBC版本一致
      
              'MARS_Connection': True,  #使用MARS (multiple active result sets)，支持异步
              }
    }
}



