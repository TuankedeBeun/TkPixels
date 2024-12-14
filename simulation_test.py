from TkPixels.Board import Board

board = Board(0.8, pixelradius = 10)
board.strips[0].fill((255, 0, 0))
board.strips[1].fill((0, 0, 255))
board.strips[0].show()
board.strips[1].show()
board.root.mainloop()