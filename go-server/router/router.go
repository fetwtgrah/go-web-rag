package router

import (
	"go-web-rag/go-server/controller"

	"github.com/gin-gonic/gin"
)

func StartRouter() *gin.Engine {
	r := gin.Default()
	v1 := r.Group("/api/v1")
	{
		v1.POST("/chat", controller.AddChat)
		v1.POST("/chunk/:path", controller.GetAllChunks)
		v1.POST("/qus", controller.DealQuestion)
	}
	return r
}
