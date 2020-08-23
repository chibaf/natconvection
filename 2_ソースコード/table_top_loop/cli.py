'''
実際のエントリポイント（開始関数）
'''
def main():
    import sys
    from .loop_operator import start
    from .app_exception import AppException
    if len(sys.argv) == 1:
        try:
            start()
        except AppException as e:
            print('Error occurred.')
            print(e)

    else:
        print('arguments error', file=sys.stderr)
        sys.exit(1)



if __name__ == '__main__':
    main()
