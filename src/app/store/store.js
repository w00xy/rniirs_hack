import { defineStore } from 'pinia'

export const useNewsDataStore = defineStore('counter', {
  state: () => {
    // Загружаем избранные новости из localStorage при инициализации
    const savedFavorites = localStorage.getItem('favoritesNews')
    return { 
      news: null,
      favorites: savedFavorites ? JSON.parse(savedFavorites) : []
    }
  },
  actions: {
    updateNews(newNews) {
      this.news = newNews
      
      // Обновляем is_liked флаг для новостей на основе favorites
      if (this.news && this.favorites.length > 0) {
        this.news.forEach(news => {
          news.is_liked = this.favorites.includes(news.id)
        })
      }
    },
    // Добавление новости в избранное
    addToFavorites(newsId) {
      if (!this.favorites.includes(newsId)) {
        this.favorites.push(newsId)
        // Обновляем флаг is_liked в массиве новостей
        if (this.news) {
          const newsItem = this.news.find(item => item.id === newsId)
          if (newsItem) {
            newsItem.is_liked = true
          }
        }
        // Сохраняем в localStorage
        localStorage.setItem('favoritesNews', JSON.stringify(this.favorites))
      }
    },
    // Удаление новости из избранного
    removeFromFavorites(newsId) {
      this.favorites = this.favorites.filter(id => id !== newsId)
      // Обновляем флаг is_liked в массиве новостей
      if (this.news) {
        const newsItem = this.news.find(item => item.id === newsId)
        if (newsItem) {
          newsItem.is_liked = false
        }
      }
      // Сохраняем в localStorage
      localStorage.setItem('favoritesNews', JSON.stringify(this.favorites))
    },
    // Получение избранных новостей
    getFavoriteNews() {
      if (!this.news) return []
      return this.news.filter(news => this.favorites.includes(news.id))
    },
    // Переключение состояния избранного
    toggleFavorite(newsId) {
      if (this.favorites.includes(newsId)) {
        this.removeFromFavorites(newsId)
      } else {
        this.addToFavorites(newsId)
      }
    }
  },
})

export const useCategoriesStore = defineStore('categories', {
  state: () => {
    // Получаем сохраненные категории из localStorage или используем значения по умолчанию
    const savedCategories = localStorage.getItem('newsCategories')
    return {
      categories: savedCategories ? JSON.parse(savedCategories) : {
        category: null,
        city: null,
        sort: null,
      }
    }
  },
  actions: {
    updateCategories(newCategories) {
      this.categories = newCategories
      // Сохраняем в localStorage при каждом обновлении
      localStorage.setItem('newsCategories', JSON.stringify(newCategories))
    },
  },
})
