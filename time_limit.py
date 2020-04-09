'''来源于https://www.cnblogs.com/lyxdw/p/10033118.html，修改了部分内容'''
import time
import threading


class MyThread(threading.Thread):
    '''线程类'''
    def __init__(self, target, args=()):
        super(MyThread, self).__init__()
        self.func = target
        self.args = args
        self.running = True

    def run(self):
        # 接受返回值
        i = 0
        while self.running:
            if i < 1:
                self.result = self.func(*self.args)
            if i == 1:
                self.stop()
            i += 1

    def stop(self):
        '''停止线程'''
        self.running = False

    def get_result(self):
        '''线程不结束,返回值为None'''
        try:
            return self.result
        except Exception:
            return 0


# 为了限制真实请求时间或函数执行时间的装饰器
def limit_decor(limit_time):
    """
    limit_time: 设置最大允许执行时长,单位:秒
    未超时返回被装饰函数返回1,超时则返回 0
    """
    def functions(func):
        # 执行操作
        def run(*params):
            thre_func = MyThread(target=func, args=params)
            # 主线程结束(超出时长),则线程方法结束
            thre_func.setDaemon(True)
            thre_func.start()
            # 计算分段沉睡次数
            sleep_num = int(limit_time // 0.1)
            # 多次短暂沉睡并尝试获取返回值
            for i in range(sleep_num):
                time.sleep(0.1)
                infor = thre_func.get_result()
                if infor:
                    return 1
            # 最终返回值(不论线程是否已结束)
            if thre_func.get_result():
                return 1
            else:
                return 0  #超时返回  可以自定义
        return run
    return functions
