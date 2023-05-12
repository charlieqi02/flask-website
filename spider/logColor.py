class LogC():
    """
    Make message with color
    debug: purple
    info: green
    warning: yellow
    error: red
    """
    @staticmethod
    def debug(message):
    	# debug, purple
        return "\033[0;35m" + message + "\033[0m"

    @staticmethod
    def info(message):
    	# info, green
        return "\033[0;32m" + message + "\033[0m"

    @staticmethod
    def warning(message):
    	# warning, yellow
        return "\033[0;33m" + message + "\033[0m"

    @staticmethod
    def error(message):
    	# error, red
        return "\033[0;31m" + message + "\033[0m"
