package controller

import (
	"bytes"
	"encoding/json"
	"go-web-rag/go-server/model"
	"io"
	"net/http"

	"github.com/gin-gonic/gin"
)

func AddChat(c *gin.Context) {
	var req model.ChatRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	jsondata, err := json.Marshal(map[string]string{
		"content": req.Content,
	})
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	resp, err := http.Post("http://localhost:8000/chat", "application/json", bytes.NewBuffer(jsondata))
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	var result map[string]string
	if err := json.Unmarshal(body, &result); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"msg":    result["msg"],
		"answer": result["ans"],
	})
}
