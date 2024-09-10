{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Content Based Recommender System"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 150,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np \n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 151,
   "metadata": {},
   "outputs": [],
   "source": [
    "movies = pd.read_csv('data/tmdb_5000_movies.csv')\n",
    "credits = pd.read_csv('data/tmdb_5000_credits.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 152,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>budget</th>\n",
       "      <th>genres</th>\n",
       "      <th>homepage</th>\n",
       "      <th>id</th>\n",
       "      <th>keywords</th>\n",
       "      <th>original_language</th>\n",
       "      <th>original_title</th>\n",
       "      <th>overview</th>\n",
       "      <th>popularity</th>\n",
       "      <th>production_companies</th>\n",
       "      <th>production_countries</th>\n",
       "      <th>release_date</th>\n",
       "      <th>revenue</th>\n",
       "      <th>runtime</th>\n",
       "      <th>spoken_languages</th>\n",
       "      <th>status</th>\n",
       "      <th>tagline</th>\n",
       "      <th>title</th>\n",
       "      <th>vote_average</th>\n",
       "      <th>vote_count</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>237000000</td>\n",
       "      <td>[{\"id\": 28, \"name\": \"Action\"}, {\"id\": 12, \"nam...</td>\n",
       "      <td>http://www.avatarmovie.com/</td>\n",
       "      <td>19995</td>\n",
       "      <td>[{\"id\": 1463, \"name\": \"culture clash\"}, {\"id\":...</td>\n",
       "      <td>en</td>\n",
       "      <td>Avatar</td>\n",
       "      <td>In the 22nd century, a paraplegic Marine is di...</td>\n",
       "      <td>150.437577</td>\n",
       "      <td>[{\"name\": \"Ingenious Film Partners\", \"id\": 289...</td>\n",
       "      <td>[{\"iso_3166_1\": \"US\", \"name\": \"United States o...</td>\n",
       "      <td>2009-12-10</td>\n",
       "      <td>2787965087</td>\n",
       "      <td>162.0</td>\n",
       "      <td>[{\"iso_639_1\": \"en\", \"name\": \"English\"}, {\"iso...</td>\n",
       "      <td>Released</td>\n",
       "      <td>Enter the World of Pandora.</td>\n",
       "      <td>Avatar</td>\n",
       "      <td>7.2</td>\n",
       "      <td>11800</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>300000000</td>\n",
       "      <td>[{\"id\": 12, \"name\": \"Adventure\"}, {\"id\": 14, \"...</td>\n",
       "      <td>http://disney.go.com/disneypictures/pirates/</td>\n",
       "      <td>285</td>\n",
       "      <td>[{\"id\": 270, \"name\": \"ocean\"}, {\"id\": 726, \"na...</td>\n",
       "      <td>en</td>\n",
       "      <td>Pirates of the Caribbean: At World's End</td>\n",
       "      <td>Captain Barbossa, long believed to be dead, ha...</td>\n",
       "      <td>139.082615</td>\n",
       "      <td>[{\"name\": \"Walt Disney Pictures\", \"id\": 2}, {\"...</td>\n",
       "      <td>[{\"iso_3166_1\": \"US\", \"name\": \"United States o...</td>\n",
       "      <td>2007-05-19</td>\n",
       "      <td>961000000</td>\n",
       "      <td>169.0</td>\n",
       "      <td>[{\"iso_639_1\": \"en\", \"name\": \"English\"}]</td>\n",
       "      <td>Released</td>\n",
       "      <td>At the end of the world, the adventure begins.</td>\n",
       "      <td>Pirates of the Caribbean: At World's End</td>\n",
       "      <td>6.9</td>\n",
       "      <td>4500</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "      budget                                             genres  \\\n",
       "0  237000000  [{\"id\": 28, \"name\": \"Action\"}, {\"id\": 12, \"nam...   \n",
       "1  300000000  [{\"id\": 12, \"name\": \"Adventure\"}, {\"id\": 14, \"...   \n",
       "\n",
       "                                       homepage     id  \\\n",
       "0                   http://www.avatarmovie.com/  19995   \n",
       "1  http://disney.go.com/disneypictures/pirates/    285   \n",
       "\n",
       "                                            keywords original_language  \\\n",
       "0  [{\"id\": 1463, \"name\": \"culture clash\"}, {\"id\":...                en   \n",
       "1  [{\"id\": 270, \"name\": \"ocean\"}, {\"id\": 726, \"na...                en   \n",
       "\n",
       "                             original_title  \\\n",
       "0                                    Avatar   \n",
       "1  Pirates of the Caribbean: At World's End   \n",
       "\n",
       "                                            overview  popularity  \\\n",
       "0  In the 22nd century, a paraplegic Marine is di...  150.437577   \n",
       "1  Captain Barbossa, long believed to be dead, ha...  139.082615   \n",
       "\n",
       "                                production_companies  \\\n",
       "0  [{\"name\": \"Ingenious Film Partners\", \"id\": 289...   \n",
       "1  [{\"name\": \"Walt Disney Pictures\", \"id\": 2}, {\"...   \n",
       "\n",
       "                                production_countries release_date     revenue  \\\n",
       "0  [{\"iso_3166_1\": \"US\", \"name\": \"United States o...   2009-12-10  2787965087   \n",
       "1  [{\"iso_3166_1\": \"US\", \"name\": \"United States o...   2007-05-19   961000000   \n",
       "\n",
       "   runtime                                   spoken_languages    status  \\\n",
       "0    162.0  [{\"iso_639_1\": \"en\", \"name\": \"English\"}, {\"iso...  Released   \n",
       "1    169.0           [{\"iso_639_1\": \"en\", \"name\": \"English\"}]  Released   \n",
       "\n",
       "                                          tagline  \\\n",
       "0                     Enter the World of Pandora.   \n",
       "1  At the end of the world, the adventure begins.   \n",
       "\n",
       "                                      title  vote_average  vote_count  \n",
       "0                                    Avatar           7.2       11800  \n",
       "1  Pirates of the Caribbean: At World's End           6.9        4500  "
      ]
     },
     "execution_count": 152,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.head(2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 153,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(4803, 20)"
      ]
     },
     "execution_count": 153,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 154,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>movie_id</th>\n",
       "      <th>title</th>\n",
       "      <th>cast</th>\n",
       "      <th>crew</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>19995</td>\n",
       "      <td>Avatar</td>\n",
       "      <td>[{\"cast_id\": 242, \"character\": \"Jake Sully\", \"...</td>\n",
       "      <td>[{\"credit_id\": \"52fe48009251416c750aca23\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>285</td>\n",
       "      <td>Pirates of the Caribbean: At World's End</td>\n",
       "      <td>[{\"cast_id\": 4, \"character\": \"Captain Jack Spa...</td>\n",
       "      <td>[{\"credit_id\": \"52fe4232c3a36847f800b579\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>206647</td>\n",
       "      <td>Spectre</td>\n",
       "      <td>[{\"cast_id\": 1, \"character\": \"James Bond\", \"cr...</td>\n",
       "      <td>[{\"credit_id\": \"54805967c3a36829b5002c41\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>49026</td>\n",
       "      <td>The Dark Knight Rises</td>\n",
       "      <td>[{\"cast_id\": 2, \"character\": \"Bruce Wayne / Ba...</td>\n",
       "      <td>[{\"credit_id\": \"52fe4781c3a36847f81398c3\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>49529</td>\n",
       "      <td>John Carter</td>\n",
       "      <td>[{\"cast_id\": 5, \"character\": \"John Carter\", \"c...</td>\n",
       "      <td>[{\"credit_id\": \"52fe479ac3a36847f813eaa3\", \"de...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   movie_id                                     title  \\\n",
       "0     19995                                    Avatar   \n",
       "1       285  Pirates of the Caribbean: At World's End   \n",
       "2    206647                                   Spectre   \n",
       "3     49026                     The Dark Knight Rises   \n",
       "4     49529                               John Carter   \n",
       "\n",
       "                                                cast  \\\n",
       "0  [{\"cast_id\": 242, \"character\": \"Jake Sully\", \"...   \n",
       "1  [{\"cast_id\": 4, \"character\": \"Captain Jack Spa...   \n",
       "2  [{\"cast_id\": 1, \"character\": \"James Bond\", \"cr...   \n",
       "3  [{\"cast_id\": 2, \"character\": \"Bruce Wayne / Ba...   \n",
       "4  [{\"cast_id\": 5, \"character\": \"John Carter\", \"c...   \n",
       "\n",
       "                                                crew  \n",
       "0  [{\"credit_id\": \"52fe48009251416c750aca23\", \"de...  \n",
       "1  [{\"credit_id\": \"52fe4232c3a36847f800b579\", \"de...  \n",
       "2  [{\"credit_id\": \"54805967c3a36829b5002c41\", \"de...  \n",
       "3  [{\"credit_id\": \"52fe4781c3a36847f81398c3\", \"de...  \n",
       "4  [{\"credit_id\": \"52fe479ac3a36847f813eaa3\", \"de...  "
      ]
     },
     "execution_count": 154,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "credits.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 155,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(4803, 4)"
      ]
     },
     "execution_count": 155,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "credits.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 156,
   "metadata": {},
   "outputs": [],
   "source": [
    "movies = movies.merge(credits,on='title')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 157,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>budget</th>\n",
       "      <th>genres</th>\n",
       "      <th>homepage</th>\n",
       "      <th>id</th>\n",
       "      <th>keywords</th>\n",
       "      <th>original_language</th>\n",
       "      <th>original_title</th>\n",
       "      <th>overview</th>\n",
       "      <th>popularity</th>\n",
       "      <th>production_companies</th>\n",
       "      <th>...</th>\n",
       "      <th>runtime</th>\n",
       "      <th>spoken_languages</th>\n",
       "      <th>status</th>\n",
       "      <th>tagline</th>\n",
       "      <th>title</th>\n",
       "      <th>vote_average</th>\n",
       "      <th>vote_count</th>\n",
       "      <th>movie_id</th>\n",
       "      <th>cast</th>\n",
       "      <th>crew</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>237000000</td>\n",
       "      <td>[{\"id\": 28, \"name\": \"Action\"}, {\"id\": 12, \"nam...</td>\n",
       "      <td>http://www.avatarmovie.com/</td>\n",
       "      <td>19995</td>\n",
       "      <td>[{\"id\": 1463, \"name\": \"culture clash\"}, {\"id\":...</td>\n",
       "      <td>en</td>\n",
       "      <td>Avatar</td>\n",
       "      <td>In the 22nd century, a paraplegic Marine is di...</td>\n",
       "      <td>150.437577</td>\n",
       "      <td>[{\"name\": \"Ingenious Film Partners\", \"id\": 289...</td>\n",
       "      <td>...</td>\n",
       "      <td>162.0</td>\n",
       "      <td>[{\"iso_639_1\": \"en\", \"name\": \"English\"}, {\"iso...</td>\n",
       "      <td>Released</td>\n",
       "      <td>Enter the World of Pandora.</td>\n",
       "      <td>Avatar</td>\n",
       "      <td>7.2</td>\n",
       "      <td>11800</td>\n",
       "      <td>19995</td>\n",
       "      <td>[{\"cast_id\": 242, \"character\": \"Jake Sully\", \"...</td>\n",
       "      <td>[{\"credit_id\": \"52fe48009251416c750aca23\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>300000000</td>\n",
       "      <td>[{\"id\": 12, \"name\": \"Adventure\"}, {\"id\": 14, \"...</td>\n",
       "      <td>http://disney.go.com/disneypictures/pirates/</td>\n",
       "      <td>285</td>\n",
       "      <td>[{\"id\": 270, \"name\": \"ocean\"}, {\"id\": 726, \"na...</td>\n",
       "      <td>en</td>\n",
       "      <td>Pirates of the Caribbean: At World's End</td>\n",
       "      <td>Captain Barbossa, long believed to be dead, ha...</td>\n",
       "      <td>139.082615</td>\n",
       "      <td>[{\"name\": \"Walt Disney Pictures\", \"id\": 2}, {\"...</td>\n",
       "      <td>...</td>\n",
       "      <td>169.0</td>\n",
       "      <td>[{\"iso_639_1\": \"en\", \"name\": \"English\"}]</td>\n",
       "      <td>Released</td>\n",
       "      <td>At the end of the world, the adventure begins.</td>\n",
       "      <td>Pirates of the Caribbean: At World's End</td>\n",
       "      <td>6.9</td>\n",
       "      <td>4500</td>\n",
       "      <td>285</td>\n",
       "      <td>[{\"cast_id\": 4, \"character\": \"Captain Jack Spa...</td>\n",
       "      <td>[{\"credit_id\": \"52fe4232c3a36847f800b579\", \"de...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>2 rows × 23 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "      budget                                             genres  \\\n",
       "0  237000000  [{\"id\": 28, \"name\": \"Action\"}, {\"id\": 12, \"nam...   \n",
       "1  300000000  [{\"id\": 12, \"name\": \"Adventure\"}, {\"id\": 14, \"...   \n",
       "\n",
       "                                       homepage     id  \\\n",
       "0                   http://www.avatarmovie.com/  19995   \n",
       "1  http://disney.go.com/disneypictures/pirates/    285   \n",
       "\n",
       "                                            keywords original_language  \\\n",
       "0  [{\"id\": 1463, \"name\": \"culture clash\"}, {\"id\":...                en   \n",
       "1  [{\"id\": 270, \"name\": \"ocean\"}, {\"id\": 726, \"na...                en   \n",
       "\n",
       "                             original_title  \\\n",
       "0                                    Avatar   \n",
       "1  Pirates of the Caribbean: At World's End   \n",
       "\n",
       "                                            overview  popularity  \\\n",
       "0  In the 22nd century, a paraplegic Marine is di...  150.437577   \n",
       "1  Captain Barbossa, long believed to be dead, ha...  139.082615   \n",
       "\n",
       "                                production_companies  ... runtime  \\\n",
       "0  [{\"name\": \"Ingenious Film Partners\", \"id\": 289...  ...   162.0   \n",
       "1  [{\"name\": \"Walt Disney Pictures\", \"id\": 2}, {\"...  ...   169.0   \n",
       "\n",
       "                                    spoken_languages    status  \\\n",
       "0  [{\"iso_639_1\": \"en\", \"name\": \"English\"}, {\"iso...  Released   \n",
       "1           [{\"iso_639_1\": \"en\", \"name\": \"English\"}]  Released   \n",
       "\n",
       "                                          tagline  \\\n",
       "0                     Enter the World of Pandora.   \n",
       "1  At the end of the world, the adventure begins.   \n",
       "\n",
       "                                      title vote_average vote_count movie_id  \\\n",
       "0                                    Avatar          7.2      11800    19995   \n",
       "1  Pirates of the Caribbean: At World's End          6.9       4500      285   \n",
       "\n",
       "                                                cast  \\\n",
       "0  [{\"cast_id\": 242, \"character\": \"Jake Sully\", \"...   \n",
       "1  [{\"cast_id\": 4, \"character\": \"Captain Jack Spa...   \n",
       "\n",
       "                                                crew  \n",
       "0  [{\"credit_id\": \"52fe48009251416c750aca23\", \"de...  \n",
       "1  [{\"credit_id\": \"52fe4232c3a36847f800b579\", \"de...  \n",
       "\n",
       "[2 rows x 23 columns]"
      ]
     },
     "execution_count": 157,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.head(2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 158,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(4809, 23)"
      ]
     },
     "execution_count": 158,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 159,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Keeping important columns for recommendation\n",
    "movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 160,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>movie_id</th>\n",
       "      <th>title</th>\n",
       "      <th>overview</th>\n",
       "      <th>genres</th>\n",
       "      <th>keywords</th>\n",
       "      <th>cast</th>\n",
       "      <th>crew</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>19995</td>\n",
       "      <td>Avatar</td>\n",
       "      <td>In the 22nd century, a paraplegic Marine is di...</td>\n",
       "      <td>[{\"id\": 28, \"name\": \"Action\"}, {\"id\": 12, \"nam...</td>\n",
       "      <td>[{\"id\": 1463, \"name\": \"culture clash\"}, {\"id\":...</td>\n",
       "      <td>[{\"cast_id\": 242, \"character\": \"Jake Sully\", \"...</td>\n",
       "      <td>[{\"credit_id\": \"52fe48009251416c750aca23\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>285</td>\n",
       "      <td>Pirates of the Caribbean: At World's End</td>\n",
       "      <td>Captain Barbossa, long believed to be dead, ha...</td>\n",
       "      <td>[{\"id\": 12, \"name\": \"Adventure\"}, {\"id\": 14, \"...</td>\n",
       "      <td>[{\"id\": 270, \"name\": \"ocean\"}, {\"id\": 726, \"na...</td>\n",
       "      <td>[{\"cast_id\": 4, \"character\": \"Captain Jack Spa...</td>\n",
       "      <td>[{\"credit_id\": \"52fe4232c3a36847f800b579\", \"de...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   movie_id                                     title  \\\n",
       "0     19995                                    Avatar   \n",
       "1       285  Pirates of the Caribbean: At World's End   \n",
       "\n",
       "                                            overview  \\\n",
       "0  In the 22nd century, a paraplegic Marine is di...   \n",
       "1  Captain Barbossa, long believed to be dead, ha...   \n",
       "\n",
       "                                              genres  \\\n",
       "0  [{\"id\": 28, \"name\": \"Action\"}, {\"id\": 12, \"nam...   \n",
       "1  [{\"id\": 12, \"name\": \"Adventure\"}, {\"id\": 14, \"...   \n",
       "\n",
       "                                            keywords  \\\n",
       "0  [{\"id\": 1463, \"name\": \"culture clash\"}, {\"id\":...   \n",
       "1  [{\"id\": 270, \"name\": \"ocean\"}, {\"id\": 726, \"na...   \n",
       "\n",
       "                                                cast  \\\n",
       "0  [{\"cast_id\": 242, \"character\": \"Jake Sully\", \"...   \n",
       "1  [{\"cast_id\": 4, \"character\": \"Captain Jack Spa...   \n",
       "\n",
       "                                                crew  \n",
       "0  [{\"credit_id\": \"52fe48009251416c750aca23\", \"de...  \n",
       "1  [{\"credit_id\": \"52fe4232c3a36847f800b579\", \"de...  "
      ]
     },
     "execution_count": 160,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.head(2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 161,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(4809, 7)"
      ]
     },
     "execution_count": 161,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 162,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "movie_id    0\n",
       "title       0\n",
       "overview    3\n",
       "genres      0\n",
       "keywords    0\n",
       "cast        0\n",
       "crew        0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 162,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.isnull().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 163,
   "metadata": {},
   "outputs": [],
   "source": [
    "movies.dropna(inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 164,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "movie_id    0\n",
       "title       0\n",
       "overview    0\n",
       "genres      0\n",
       "keywords    0\n",
       "cast        0\n",
       "crew        0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 164,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.isnull().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 165,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(4806, 7)"
      ]
     },
     "execution_count": 165,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 166,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 166,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.duplicated().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 167,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'[{\"id\": 28, \"name\": \"Action\"}, {\"id\": 12, \"name\": \"Adventure\"}, {\"id\": 14, \"name\": \"Fantasy\"}, {\"id\": 878, \"name\": \"Science Fiction\"}]'"
      ]
     },
     "execution_count": 167,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# handle genres\n",
    "\n",
    "movies.iloc[0]['genres']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 168,
   "metadata": {},
   "outputs": [],
   "source": [
    "import ast #for converting str to list\n",
    "\n",
    "def convert(text):\n",
    "    L = []\n",
    "    for i in ast.literal_eval(text):\n",
    "        L.append(i['name']) \n",
    "    return L"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 169,
   "metadata": {},
   "outputs": [],
   "source": [
    "movies['genres'] = movies['genres'].apply(convert)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 170,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>movie_id</th>\n",
       "      <th>title</th>\n",
       "      <th>overview</th>\n",
       "      <th>genres</th>\n",
       "      <th>keywords</th>\n",
       "      <th>cast</th>\n",
       "      <th>crew</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>19995</td>\n",
       "      <td>Avatar</td>\n",
       "      <td>In the 22nd century, a paraplegic Marine is di...</td>\n",
       "      <td>[Action, Adventure, Fantasy, Science Fiction]</td>\n",
       "      <td>[{\"id\": 1463, \"name\": \"culture clash\"}, {\"id\":...</td>\n",
       "      <td>[{\"cast_id\": 242, \"character\": \"Jake Sully\", \"...</td>\n",
       "      <td>[{\"credit_id\": \"52fe48009251416c750aca23\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>285</td>\n",
       "      <td>Pirates of the Caribbean: At World's End</td>\n",
       "      <td>Captain Barbossa, long believed to be dead, ha...</td>\n",
       "      <td>[Adventure, Fantasy, Action]</td>\n",
       "      <td>[{\"id\": 270, \"name\": \"ocean\"}, {\"id\": 726, \"na...</td>\n",
       "      <td>[{\"cast_id\": 4, \"character\": \"Captain Jack Spa...</td>\n",
       "      <td>[{\"credit_id\": \"52fe4232c3a36847f800b579\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>206647</td>\n",
       "      <td>Spectre</td>\n",
       "      <td>A cryptic message from Bond’s past sends him o...</td>\n",
       "      <td>[Action, Adventure, Crime]</td>\n",
       "      <td>[{\"id\": 470, \"name\": \"spy\"}, {\"id\": 818, \"name...</td>\n",
       "      <td>[{\"cast_id\": 1, \"character\": \"James Bond\", \"cr...</td>\n",
       "      <td>[{\"credit_id\": \"54805967c3a36829b5002c41\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>49026</td>\n",
       "      <td>The Dark Knight Rises</td>\n",
       "      <td>Following the death of District Attorney Harve...</td>\n",
       "      <td>[Action, Crime, Drama, Thriller]</td>\n",
       "      <td>[{\"id\": 849, \"name\": \"dc comics\"}, {\"id\": 853,...</td>\n",
       "      <td>[{\"cast_id\": 2, \"character\": \"Bruce Wayne / Ba...</td>\n",
       "      <td>[{\"credit_id\": \"52fe4781c3a36847f81398c3\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>49529</td>\n",
       "      <td>John Carter</td>\n",
       "      <td>John Carter is a war-weary, former military ca...</td>\n",
       "      <td>[Action, Adventure, Science Fiction]</td>\n",
       "      <td>[{\"id\": 818, \"name\": \"based on novel\"}, {\"id\":...</td>\n",
       "      <td>[{\"cast_id\": 5, \"character\": \"John Carter\", \"c...</td>\n",
       "      <td>[{\"credit_id\": \"52fe479ac3a36847f813eaa3\", \"de...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   movie_id                                     title  \\\n",
       "0     19995                                    Avatar   \n",
       "1       285  Pirates of the Caribbean: At World's End   \n",
       "2    206647                                   Spectre   \n",
       "3     49026                     The Dark Knight Rises   \n",
       "4     49529                               John Carter   \n",
       "\n",
       "                                            overview  \\\n",
       "0  In the 22nd century, a paraplegic Marine is di...   \n",
       "1  Captain Barbossa, long believed to be dead, ha...   \n",
       "2  A cryptic message from Bond’s past sends him o...   \n",
       "3  Following the death of District Attorney Harve...   \n",
       "4  John Carter is a war-weary, former military ca...   \n",
       "\n",
       "                                          genres  \\\n",
       "0  [Action, Adventure, Fantasy, Science Fiction]   \n",
       "1                   [Adventure, Fantasy, Action]   \n",
       "2                     [Action, Adventure, Crime]   \n",
       "3               [Action, Crime, Drama, Thriller]   \n",
       "4           [Action, Adventure, Science Fiction]   \n",
       "\n",
       "                                            keywords  \\\n",
       "0  [{\"id\": 1463, \"name\": \"culture clash\"}, {\"id\":...   \n",
       "1  [{\"id\": 270, \"name\": \"ocean\"}, {\"id\": 726, \"na...   \n",
       "2  [{\"id\": 470, \"name\": \"spy\"}, {\"id\": 818, \"name...   \n",
       "3  [{\"id\": 849, \"name\": \"dc comics\"}, {\"id\": 853,...   \n",
       "4  [{\"id\": 818, \"name\": \"based on novel\"}, {\"id\":...   \n",
       "\n",
       "                                                cast  \\\n",
       "0  [{\"cast_id\": 242, \"character\": \"Jake Sully\", \"...   \n",
       "1  [{\"cast_id\": 4, \"character\": \"Captain Jack Spa...   \n",
       "2  [{\"cast_id\": 1, \"character\": \"James Bond\", \"cr...   \n",
       "3  [{\"cast_id\": 2, \"character\": \"Bruce Wayne / Ba...   \n",
       "4  [{\"cast_id\": 5, \"character\": \"John Carter\", \"c...   \n",
       "\n",
       "                                                crew  \n",
       "0  [{\"credit_id\": \"52fe48009251416c750aca23\", \"de...  \n",
       "1  [{\"credit_id\": \"52fe4232c3a36847f800b579\", \"de...  \n",
       "2  [{\"credit_id\": \"54805967c3a36829b5002c41\", \"de...  \n",
       "3  [{\"credit_id\": \"52fe4781c3a36847f81398c3\", \"de...  \n",
       "4  [{\"credit_id\": \"52fe479ac3a36847f813eaa3\", \"de...  "
      ]
     },
     "execution_count": 170,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 171,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'[{\"id\": 1463, \"name\": \"culture clash\"}, {\"id\": 2964, \"name\": \"future\"}, {\"id\": 3386, \"name\": \"space war\"}, {\"id\": 3388, \"name\": \"space colony\"}, {\"id\": 3679, \"name\": \"society\"}, {\"id\": 3801, \"name\": \"space travel\"}, {\"id\": 9685, \"name\": \"futuristic\"}, {\"id\": 9840, \"name\": \"romance\"}, {\"id\": 9882, \"name\": \"space\"}, {\"id\": 9951, \"name\": \"alien\"}, {\"id\": 10148, \"name\": \"tribe\"}, {\"id\": 10158, \"name\": \"alien planet\"}, {\"id\": 10987, \"name\": \"cgi\"}, {\"id\": 11399, \"name\": \"marine\"}, {\"id\": 13065, \"name\": \"soldier\"}, {\"id\": 14643, \"name\": \"battle\"}, {\"id\": 14720, \"name\": \"love affair\"}, {\"id\": 165431, \"name\": \"anti war\"}, {\"id\": 193554, \"name\": \"power relations\"}, {\"id\": 206690, \"name\": \"mind and soul\"}, {\"id\": 209714, \"name\": \"3d\"}]'"
      ]
     },
     "execution_count": 171,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# handle keywords\n",
    "movies.iloc[0]['keywords']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 172,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>movie_id</th>\n",
       "      <th>title</th>\n",
       "      <th>overview</th>\n",
       "      <th>genres</th>\n",
       "      <th>keywords</th>\n",
       "      <th>cast</th>\n",
       "      <th>crew</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>19995</td>\n",
       "      <td>Avatar</td>\n",
       "      <td>In the 22nd century, a paraplegic Marine is di...</td>\n",
       "      <td>[Action, Adventure, Fantasy, Science Fiction]</td>\n",
       "      <td>[culture clash, future, space war, space colon...</td>\n",
       "      <td>[{\"cast_id\": 242, \"character\": \"Jake Sully\", \"...</td>\n",
       "      <td>[{\"credit_id\": \"52fe48009251416c750aca23\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>285</td>\n",
       "      <td>Pirates of the Caribbean: At World's End</td>\n",
       "      <td>Captain Barbossa, long believed to be dead, ha...</td>\n",
       "      <td>[Adventure, Fantasy, Action]</td>\n",
       "      <td>[ocean, drug abuse, exotic island, east india ...</td>\n",
       "      <td>[{\"cast_id\": 4, \"character\": \"Captain Jack Spa...</td>\n",
       "      <td>[{\"credit_id\": \"52fe4232c3a36847f800b579\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>206647</td>\n",
       "      <td>Spectre</td>\n",
       "      <td>A cryptic message from Bond’s past sends him o...</td>\n",
       "      <td>[Action, Adventure, Crime]</td>\n",
       "      <td>[spy, based on novel, secret agent, sequel, mi...</td>\n",
       "      <td>[{\"cast_id\": 1, \"character\": \"James Bond\", \"cr...</td>\n",
       "      <td>[{\"credit_id\": \"54805967c3a36829b5002c41\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>49026</td>\n",
       "      <td>The Dark Knight Rises</td>\n",
       "      <td>Following the death of District Attorney Harve...</td>\n",
       "      <td>[Action, Crime, Drama, Thriller]</td>\n",
       "      <td>[dc comics, crime fighter, terrorist, secret i...</td>\n",
       "      <td>[{\"cast_id\": 2, \"character\": \"Bruce Wayne / Ba...</td>\n",
       "      <td>[{\"credit_id\": \"52fe4781c3a36847f81398c3\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>49529</td>\n",
       "      <td>John Carter</td>\n",
       "      <td>John Carter is a war-weary, former military ca...</td>\n",
       "      <td>[Action, Adventure, Science Fiction]</td>\n",
       "      <td>[based on novel, mars, medallion, space travel...</td>\n",
       "      <td>[{\"cast_id\": 5, \"character\": \"John Carter\", \"c...</td>\n",
       "      <td>[{\"credit_id\": \"52fe479ac3a36847f813eaa3\", \"de...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   movie_id                                     title  \\\n",
       "0     19995                                    Avatar   \n",
       "1       285  Pirates of the Caribbean: At World's End   \n",
       "2    206647                                   Spectre   \n",
       "3     49026                     The Dark Knight Rises   \n",
       "4     49529                               John Carter   \n",
       "\n",
       "                                            overview  \\\n",
       "0  In the 22nd century, a paraplegic Marine is di...   \n",
       "1  Captain Barbossa, long believed to be dead, ha...   \n",
       "2  A cryptic message from Bond’s past sends him o...   \n",
       "3  Following the death of District Attorney Harve...   \n",
       "4  John Carter is a war-weary, former military ca...   \n",
       "\n",
       "                                          genres  \\\n",
       "0  [Action, Adventure, Fantasy, Science Fiction]   \n",
       "1                   [Adventure, Fantasy, Action]   \n",
       "2                     [Action, Adventure, Crime]   \n",
       "3               [Action, Crime, Drama, Thriller]   \n",
       "4           [Action, Adventure, Science Fiction]   \n",
       "\n",
       "                                            keywords  \\\n",
       "0  [culture clash, future, space war, space colon...   \n",
       "1  [ocean, drug abuse, exotic island, east india ...   \n",
       "2  [spy, based on novel, secret agent, sequel, mi...   \n",
       "3  [dc comics, crime fighter, terrorist, secret i...   \n",
       "4  [based on novel, mars, medallion, space travel...   \n",
       "\n",
       "                                                cast  \\\n",
       "0  [{\"cast_id\": 242, \"character\": \"Jake Sully\", \"...   \n",
       "1  [{\"cast_id\": 4, \"character\": \"Captain Jack Spa...   \n",
       "2  [{\"cast_id\": 1, \"character\": \"James Bond\", \"cr...   \n",
       "3  [{\"cast_id\": 2, \"character\": \"Bruce Wayne / Ba...   \n",
       "4  [{\"cast_id\": 5, \"character\": \"John Carter\", \"c...   \n",
       "\n",
       "                                                crew  \n",
       "0  [{\"credit_id\": \"52fe48009251416c750aca23\", \"de...  \n",
       "1  [{\"credit_id\": \"52fe4232c3a36847f800b579\", \"de...  \n",
       "2  [{\"credit_id\": \"54805967c3a36829b5002c41\", \"de...  \n",
       "3  [{\"credit_id\": \"52fe4781c3a36847f81398c3\", \"de...  \n",
       "4  [{\"credit_id\": \"52fe479ac3a36847f813eaa3\", \"de...  "
      ]
     },
     "execution_count": 172,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies['keywords'] = movies['keywords'].apply(convert)\n",
    "movies.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 173,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'[{\"cast_id\": 242, \"character\": \"Jake Sully\", \"credit_id\": \"5602a8a7c3a3685532001c9a\", \"gender\": 2, \"id\": 65731, \"name\": \"Sam Worthington\", \"order\": 0}, {\"cast_id\": 3, \"character\": \"Neytiri\", \"credit_id\": \"52fe48009251416c750ac9cb\", \"gender\": 1, \"id\": 8691, \"name\": \"Zoe Saldana\", \"order\": 1}, {\"cast_id\": 25, \"character\": \"Dr. Grace Augustine\", \"credit_id\": \"52fe48009251416c750aca39\", \"gender\": 1, \"id\": 10205, \"name\": \"Sigourney Weaver\", \"order\": 2}, {\"cast_id\": 4, \"character\": \"Col. Quaritch\", \"credit_id\": \"52fe48009251416c750ac9cf\", \"gender\": 2, \"id\": 32747, \"name\": \"Stephen Lang\", \"order\": 3}, {\"cast_id\": 5, \"character\": \"Trudy Chacon\", \"credit_id\": \"52fe48009251416c750ac9d3\", \"gender\": 1, \"id\": 17647, \"name\": \"Michelle Rodriguez\", \"order\": 4}, {\"cast_id\": 8, \"character\": \"Selfridge\", \"credit_id\": \"52fe48009251416c750ac9e1\", \"gender\": 2, \"id\": 1771, \"name\": \"Giovanni Ribisi\", \"order\": 5}, {\"cast_id\": 7, \"character\": \"Norm Spellman\", \"credit_id\": \"52fe48009251416c750ac9dd\", \"gender\": 2, \"id\": 59231, \"name\": \"Joel David Moore\", \"order\": 6}, {\"cast_id\": 9, \"character\": \"Moat\", \"credit_id\": \"52fe48009251416c750ac9e5\", \"gender\": 1, \"id\": 30485, \"name\": \"CCH Pounder\", \"order\": 7}, {\"cast_id\": 11, \"character\": \"Eytukan\", \"credit_id\": \"52fe48009251416c750ac9ed\", \"gender\": 2, \"id\": 15853, \"name\": \"Wes Studi\", \"order\": 8}, {\"cast_id\": 10, \"character\": \"Tsu\\'Tey\", \"credit_id\": \"52fe48009251416c750ac9e9\", \"gender\": 2, \"id\": 10964, \"name\": \"Laz Alonso\", \"order\": 9}, {\"cast_id\": 12, \"character\": \"Dr. Max Patel\", \"credit_id\": \"52fe48009251416c750ac9f1\", \"gender\": 2, \"id\": 95697, \"name\": \"Dileep Rao\", \"order\": 10}, {\"cast_id\": 13, \"character\": \"Lyle Wainfleet\", \"credit_id\": \"52fe48009251416c750ac9f5\", \"gender\": 2, \"id\": 98215, \"name\": \"Matt Gerald\", \"order\": 11}, {\"cast_id\": 32, \"character\": \"Private Fike\", \"credit_id\": \"52fe48009251416c750aca5b\", \"gender\": 2, \"id\": 154153, \"name\": \"Sean Anthony Moran\", \"order\": 12}, {\"cast_id\": 33, \"character\": \"Cryo Vault Med Tech\", \"credit_id\": \"52fe48009251416c750aca5f\", \"gender\": 2, \"id\": 397312, \"name\": \"Jason Whyte\", \"order\": 13}, {\"cast_id\": 34, \"character\": \"Venture Star Crew Chief\", \"credit_id\": \"52fe48009251416c750aca63\", \"gender\": 2, \"id\": 42317, \"name\": \"Scott Lawrence\", \"order\": 14}, {\"cast_id\": 35, \"character\": \"Lock Up Trooper\", \"credit_id\": \"52fe48009251416c750aca67\", \"gender\": 2, \"id\": 986734, \"name\": \"Kelly Kilgour\", \"order\": 15}, {\"cast_id\": 36, \"character\": \"Shuttle Pilot\", \"credit_id\": \"52fe48009251416c750aca6b\", \"gender\": 0, \"id\": 1207227, \"name\": \"James Patrick Pitt\", \"order\": 16}, {\"cast_id\": 37, \"character\": \"Shuttle Co-Pilot\", \"credit_id\": \"52fe48009251416c750aca6f\", \"gender\": 0, \"id\": 1180936, \"name\": \"Sean Patrick Murphy\", \"order\": 17}, {\"cast_id\": 38, \"character\": \"Shuttle Crew Chief\", \"credit_id\": \"52fe48009251416c750aca73\", \"gender\": 2, \"id\": 1019578, \"name\": \"Peter Dillon\", \"order\": 18}, {\"cast_id\": 39, \"character\": \"Tractor Operator / Troupe\", \"credit_id\": \"52fe48009251416c750aca77\", \"gender\": 0, \"id\": 91443, \"name\": \"Kevin Dorman\", \"order\": 19}, {\"cast_id\": 40, \"character\": \"Dragon Gunship Pilot\", \"credit_id\": \"52fe48009251416c750aca7b\", \"gender\": 2, \"id\": 173391, \"name\": \"Kelson Henderson\", \"order\": 20}, {\"cast_id\": 41, \"character\": \"Dragon Gunship Gunner\", \"credit_id\": \"52fe48009251416c750aca7f\", \"gender\": 0, \"id\": 1207236, \"name\": \"David Van Horn\", \"order\": 21}, {\"cast_id\": 42, \"character\": \"Dragon Gunship Navigator\", \"credit_id\": \"52fe48009251416c750aca83\", \"gender\": 0, \"id\": 215913, \"name\": \"Jacob Tomuri\", \"order\": 22}, {\"cast_id\": 43, \"character\": \"Suit #1\", \"credit_id\": \"52fe48009251416c750aca87\", \"gender\": 0, \"id\": 143206, \"name\": \"Michael Blain-Rozgay\", \"order\": 23}, {\"cast_id\": 44, \"character\": \"Suit #2\", \"credit_id\": \"52fe48009251416c750aca8b\", \"gender\": 2, \"id\": 169676, \"name\": \"Jon Curry\", \"order\": 24}, {\"cast_id\": 46, \"character\": \"Ambient Room Tech\", \"credit_id\": \"52fe48009251416c750aca8f\", \"gender\": 0, \"id\": 1048610, \"name\": \"Luke Hawker\", \"order\": 25}, {\"cast_id\": 47, \"character\": \"Ambient Room Tech / Troupe\", \"credit_id\": \"52fe48009251416c750aca93\", \"gender\": 0, \"id\": 42288, \"name\": \"Woody Schultz\", \"order\": 26}, {\"cast_id\": 48, \"character\": \"Horse Clan Leader\", \"credit_id\": \"52fe48009251416c750aca97\", \"gender\": 2, \"id\": 68278, \"name\": \"Peter Mensah\", \"order\": 27}, {\"cast_id\": 49, \"character\": \"Link Room Tech\", \"credit_id\": \"52fe48009251416c750aca9b\", \"gender\": 0, \"id\": 1207247, \"name\": \"Sonia Yee\", \"order\": 28}, {\"cast_id\": 50, \"character\": \"Basketball Avatar / Troupe\", \"credit_id\": \"52fe48009251416c750aca9f\", \"gender\": 1, \"id\": 1207248, \"name\": \"Jahnel Curfman\", \"order\": 29}, {\"cast_id\": 51, \"character\": \"Basketball Avatar\", \"credit_id\": \"52fe48009251416c750acaa3\", \"gender\": 0, \"id\": 89714, \"name\": \"Ilram Choi\", \"order\": 30}, {\"cast_id\": 52, \"character\": \"Na\\'vi Child\", \"credit_id\": \"52fe48009251416c750acaa7\", \"gender\": 0, \"id\": 1207249, \"name\": \"Kyla Warren\", \"order\": 31}, {\"cast_id\": 53, \"character\": \"Troupe\", \"credit_id\": \"52fe48009251416c750acaab\", \"gender\": 0, \"id\": 1207250, \"name\": \"Lisa Roumain\", \"order\": 32}, {\"cast_id\": 54, \"character\": \"Troupe\", \"credit_id\": \"52fe48009251416c750acaaf\", \"gender\": 1, \"id\": 83105, \"name\": \"Debra Wilson\", \"order\": 33}, {\"cast_id\": 57, \"character\": \"Troupe\", \"credit_id\": \"52fe48009251416c750acabb\", \"gender\": 0, \"id\": 1207253, \"name\": \"Chris Mala\", \"order\": 34}, {\"cast_id\": 55, \"character\": \"Troupe\", \"credit_id\": \"52fe48009251416c750acab3\", \"gender\": 0, \"id\": 1207251, \"name\": \"Taylor Kibby\", \"order\": 35}, {\"cast_id\": 56, \"character\": \"Troupe\", \"credit_id\": \"52fe48009251416c750acab7\", \"gender\": 0, \"id\": 1207252, \"name\": \"Jodie Landau\", \"order\": 36}, {\"cast_id\": 58, \"character\": \"Troupe\", \"credit_id\": \"52fe48009251416c750acabf\", \"gender\": 0, \"id\": 1207254, \"name\": \"Julie Lamm\", \"order\": 37}, {\"cast_id\": 59, \"character\": \"Troupe\", \"credit_id\": \"52fe48009251416c750acac3\", \"gender\": 0, \"id\": 1207257, \"name\": \"Cullen B. Madden\", \"order\": 38}, {\"cast_id\": 60, \"character\": \"Troupe\", \"credit_id\": \"52fe48009251416c750acac7\", \"gender\": 0, \"id\": 1207259, \"name\": \"Joseph Brady Madden\", \"order\": 39}, {\"cast_id\": 61, \"character\": \"Troupe\", \"credit_id\": \"52fe48009251416c750acacb\", \"gender\": 0, \"id\": 1207262, \"name\": \"Frankie Torres\", \"order\": 40}, {\"cast_id\": 62, \"character\": \"Troupe\", \"credit_id\": \"52fe48009251416c750acacf\", \"gender\": 1, \"id\": 1158600, \"name\": \"Austin Wilson\", \"order\": 41}, {\"cast_id\": 63, \"character\": \"Troupe\", \"credit_id\": \"52fe48019251416c750acad3\", \"gender\": 1, \"id\": 983705, \"name\": \"Sara Wilson\", \"order\": 42}, {\"cast_id\": 64, \"character\": \"Troupe\", \"credit_id\": \"52fe48019251416c750acad7\", \"gender\": 0, \"id\": 1207263, \"name\": \"Tamica Washington-Miller\", \"order\": 43}, {\"cast_id\": 65, \"character\": \"Op Center Staff\", \"credit_id\": \"52fe48019251416c750acadb\", \"gender\": 1, \"id\": 1145098, \"name\": \"Lucy Briant\", \"order\": 44}, {\"cast_id\": 66, \"character\": \"Op Center Staff\", \"credit_id\": \"52fe48019251416c750acadf\", \"gender\": 2, \"id\": 33305, \"name\": \"Nathan Meister\", \"order\": 45}, {\"cast_id\": 67, \"character\": \"Op Center Staff\", \"credit_id\": \"52fe48019251416c750acae3\", \"gender\": 0, \"id\": 1207264, \"name\": \"Gerry Blair\", \"order\": 46}, {\"cast_id\": 68, \"character\": \"Op Center Staff\", \"credit_id\": \"52fe48019251416c750acae7\", \"gender\": 2, \"id\": 33311, \"name\": \"Matthew Chamberlain\", \"order\": 47}, {\"cast_id\": 69, \"character\": \"Op Center Staff\", \"credit_id\": \"52fe48019251416c750acaeb\", \"gender\": 0, \"id\": 1207265, \"name\": \"Paul Yates\", \"order\": 48}, {\"cast_id\": 70, \"character\": \"Op Center Duty Officer\", \"credit_id\": \"52fe48019251416c750acaef\", \"gender\": 0, \"id\": 1207266, \"name\": \"Wray Wilson\", \"order\": 49}, {\"cast_id\": 71, \"character\": \"Op Center Staff\", \"credit_id\": \"52fe48019251416c750acaf3\", \"gender\": 2, \"id\": 54492, \"name\": \"James Gaylyn\", \"order\": 50}, {\"cast_id\": 72, \"character\": \"Dancer\", \"credit_id\": \"52fe48019251416c750acaf7\", \"gender\": 0, \"id\": 1207267, \"name\": \"Melvin Leno Clark III\", \"order\": 51}, {\"cast_id\": 73, \"character\": \"Dancer\", \"credit_id\": \"52fe48019251416c750acafb\", \"gender\": 0, \"id\": 1207268, \"name\": \"Carvon Futrell\", \"order\": 52}, {\"cast_id\": 74, \"character\": \"Dancer\", \"credit_id\": \"52fe48019251416c750acaff\", \"gender\": 0, \"id\": 1207269, \"name\": \"Brandon Jelkes\", \"order\": 53}, {\"cast_id\": 75, \"character\": \"Dancer\", \"credit_id\": \"52fe48019251416c750acb03\", \"gender\": 0, \"id\": 1207270, \"name\": \"Micah Moch\", \"order\": 54}, {\"cast_id\": 76, \"character\": \"Dancer\", \"credit_id\": \"52fe48019251416c750acb07\", \"gender\": 0, \"id\": 1207271, \"name\": \"Hanniyah Muhammad\", \"order\": 55}, {\"cast_id\": 77, \"character\": \"Dancer\", \"credit_id\": \"52fe48019251416c750acb0b\", \"gender\": 0, \"id\": 1207272, \"name\": \"Christopher Nolen\", \"order\": 56}, {\"cast_id\": 78, \"character\": \"Dancer\", \"credit_id\": \"52fe48019251416c750acb0f\", \"gender\": 0, \"id\": 1207273, \"name\": \"Christa Oliver\", \"order\": 57}, {\"cast_id\": 79, \"character\": \"Dancer\", \"credit_id\": \"52fe48019251416c750acb13\", \"gender\": 0, \"id\": 1207274, \"name\": \"April Marie Thomas\", \"order\": 58}, {\"cast_id\": 80, \"character\": \"Dancer\", \"credit_id\": \"52fe48019251416c750acb17\", \"gender\": 0, \"id\": 1207275, \"name\": \"Bravita A. Threatt\", \"order\": 59}, {\"cast_id\": 81, \"character\": \"Mining Chief (uncredited)\", \"credit_id\": \"52fe48019251416c750acb1b\", \"gender\": 0, \"id\": 1207276, \"name\": \"Colin Bleasdale\", \"order\": 60}, {\"cast_id\": 82, \"character\": \"Veteran Miner (uncredited)\", \"credit_id\": \"52fe48019251416c750acb1f\", \"gender\": 0, \"id\": 107969, \"name\": \"Mike Bodnar\", \"order\": 61}, {\"cast_id\": 83, \"character\": \"Richard (uncredited)\", \"credit_id\": \"52fe48019251416c750acb23\", \"gender\": 0, \"id\": 1207278, \"name\": \"Matt Clayton\", \"order\": 62}, {\"cast_id\": 84, \"character\": \"Nav\\'i (uncredited)\", \"credit_id\": \"52fe48019251416c750acb27\", \"gender\": 1, \"id\": 147898, \"name\": \"Nicole Dionne\", \"order\": 63}, {\"cast_id\": 85, \"character\": \"Trooper (uncredited)\", \"credit_id\": \"52fe48019251416c750acb2b\", \"gender\": 0, \"id\": 1207280, \"name\": \"Jamie Harrison\", \"order\": 64}, {\"cast_id\": 86, \"character\": \"Trooper (uncredited)\", \"credit_id\": \"52fe48019251416c750acb2f\", \"gender\": 0, \"id\": 1207281, \"name\": \"Allan Henry\", \"order\": 65}, {\"cast_id\": 87, \"character\": \"Ground Technician (uncredited)\", \"credit_id\": \"52fe48019251416c750acb33\", \"gender\": 2, \"id\": 1207282, \"name\": \"Anthony Ingruber\", \"order\": 66}, {\"cast_id\": 88, \"character\": \"Flight Crew Mechanic (uncredited)\", \"credit_id\": \"52fe48019251416c750acb37\", \"gender\": 0, \"id\": 1207283, \"name\": \"Ashley Jeffery\", \"order\": 67}, {\"cast_id\": 14, \"character\": \"Samson Pilot\", \"credit_id\": \"52fe48009251416c750ac9f9\", \"gender\": 0, \"id\": 98216, \"name\": \"Dean Knowsley\", \"order\": 68}, {\"cast_id\": 89, \"character\": \"Trooper (uncredited)\", \"credit_id\": \"52fe48019251416c750acb3b\", \"gender\": 0, \"id\": 1201399, \"name\": \"Joseph Mika-Hunt\", \"order\": 69}, {\"cast_id\": 90, \"character\": \"Banshee (uncredited)\", \"credit_id\": \"52fe48019251416c750acb3f\", \"gender\": 0, \"id\": 236696, \"name\": \"Terry Notary\", \"order\": 70}, {\"cast_id\": 91, \"character\": \"Soldier (uncredited)\", \"credit_id\": \"52fe48019251416c750acb43\", \"gender\": 0, \"id\": 1207287, \"name\": \"Kai Pantano\", \"order\": 71}, {\"cast_id\": 92, \"character\": \"Blast Technician (uncredited)\", \"credit_id\": \"52fe48019251416c750acb47\", \"gender\": 0, \"id\": 1207288, \"name\": \"Logan Pithyou\", \"order\": 72}, {\"cast_id\": 93, \"character\": \"Vindum Raah (uncredited)\", \"credit_id\": \"52fe48019251416c750acb4b\", \"gender\": 0, \"id\": 1207289, \"name\": \"Stuart Pollock\", \"order\": 73}, {\"cast_id\": 94, \"character\": \"Hero (uncredited)\", \"credit_id\": \"52fe48019251416c750acb4f\", \"gender\": 0, \"id\": 584868, \"name\": \"Raja\", \"order\": 74}, {\"cast_id\": 95, \"character\": \"Ops Centreworker (uncredited)\", \"credit_id\": \"52fe48019251416c750acb53\", \"gender\": 0, \"id\": 1207290, \"name\": \"Gareth Ruck\", \"order\": 75}, {\"cast_id\": 96, \"character\": \"Engineer (uncredited)\", \"credit_id\": \"52fe48019251416c750acb57\", \"gender\": 0, \"id\": 1062463, \"name\": \"Rhian Sheehan\", \"order\": 76}, {\"cast_id\": 97, \"character\": \"Col. Quaritch\\'s Mech Suit (uncredited)\", \"credit_id\": \"52fe48019251416c750acb5b\", \"gender\": 0, \"id\": 60656, \"name\": \"T. J. Storm\", \"order\": 77}, {\"cast_id\": 98, \"character\": \"Female Marine (uncredited)\", \"credit_id\": \"52fe48019251416c750acb5f\", \"gender\": 0, \"id\": 1207291, \"name\": \"Jodie Taylor\", \"order\": 78}, {\"cast_id\": 99, \"character\": \"Ikran Clan Leader (uncredited)\", \"credit_id\": \"52fe48019251416c750acb63\", \"gender\": 1, \"id\": 1186027, \"name\": \"Alicia Vela-Bailey\", \"order\": 79}, {\"cast_id\": 100, \"character\": \"Geologist (uncredited)\", \"credit_id\": \"52fe48019251416c750acb67\", \"gender\": 0, \"id\": 1207292, \"name\": \"Richard Whiteside\", \"order\": 80}, {\"cast_id\": 101, \"character\": \"Na\\'vi (uncredited)\", \"credit_id\": \"52fe48019251416c750acb6b\", \"gender\": 0, \"id\": 103259, \"name\": \"Nikie Zambo\", \"order\": 81}, {\"cast_id\": 102, \"character\": \"Ambient Room Tech / Troupe\", \"credit_id\": \"52fe48019251416c750acb6f\", \"gender\": 1, \"id\": 42286, \"name\": \"Julene Renee\", \"order\": 82}]'"
      ]
     },
     "execution_count": 173,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# handle cast\n",
    "movies.iloc[0]['cast']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 174,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Here i am just keeping top 3 cast\n",
    "\n",
    "def convert_cast(text):\n",
    "    L = []\n",
    "    counter = 0\n",
    "    for i in ast.literal_eval(text):\n",
    "        if counter < 3:\n",
    "            L.append(i['name'])\n",
    "        counter+=1\n",
    "    return L"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 175,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>movie_id</th>\n",
       "      <th>title</th>\n",
       "      <th>overview</th>\n",
       "      <th>genres</th>\n",
       "      <th>keywords</th>\n",
       "      <th>cast</th>\n",
       "      <th>crew</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>19995</td>\n",
       "      <td>Avatar</td>\n",
       "      <td>In the 22nd century, a paraplegic Marine is di...</td>\n",
       "      <td>[Action, Adventure, Fantasy, Science Fiction]</td>\n",
       "      <td>[culture clash, future, space war, space colon...</td>\n",
       "      <td>[Sam Worthington, Zoe Saldana, Sigourney Weaver]</td>\n",
       "      <td>[{\"credit_id\": \"52fe48009251416c750aca23\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>285</td>\n",
       "      <td>Pirates of the Caribbean: At World's End</td>\n",
       "      <td>Captain Barbossa, long believed to be dead, ha...</td>\n",
       "      <td>[Adventure, Fantasy, Action]</td>\n",
       "      <td>[ocean, drug abuse, exotic island, east india ...</td>\n",
       "      <td>[Johnny Depp, Orlando Bloom, Keira Knightley]</td>\n",
       "      <td>[{\"credit_id\": \"52fe4232c3a36847f800b579\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>206647</td>\n",
       "      <td>Spectre</td>\n",
       "      <td>A cryptic message from Bond’s past sends him o...</td>\n",
       "      <td>[Action, Adventure, Crime]</td>\n",
       "      <td>[spy, based on novel, secret agent, sequel, mi...</td>\n",
       "      <td>[Daniel Craig, Christoph Waltz, Léa Seydoux]</td>\n",
       "      <td>[{\"credit_id\": \"54805967c3a36829b5002c41\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>49026</td>\n",
       "      <td>The Dark Knight Rises</td>\n",
       "      <td>Following the death of District Attorney Harve...</td>\n",
       "      <td>[Action, Crime, Drama, Thriller]</td>\n",
       "      <td>[dc comics, crime fighter, terrorist, secret i...</td>\n",
       "      <td>[Christian Bale, Michael Caine, Gary Oldman]</td>\n",
       "      <td>[{\"credit_id\": \"52fe4781c3a36847f81398c3\", \"de...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>49529</td>\n",
       "      <td>John Carter</td>\n",
       "      <td>John Carter is a war-weary, former military ca...</td>\n",
       "      <td>[Action, Adventure, Science Fiction]</td>\n",
       "      <td>[based on novel, mars, medallion, space travel...</td>\n",
       "      <td>[Taylor Kitsch, Lynn Collins, Samantha Morton]</td>\n",
       "      <td>[{\"credit_id\": \"52fe479ac3a36847f813eaa3\", \"de...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   movie_id                                     title  \\\n",
       "0     19995                                    Avatar   \n",
       "1       285  Pirates of the Caribbean: At World's End   \n",
       "2    206647                                   Spectre   \n",
       "3     49026                     The Dark Knight Rises   \n",
       "4     49529                               John Carter   \n",
       "\n",
       "                                            overview  \\\n",
       "0  In the 22nd century, a paraplegic Marine is di...   \n",
       "1  Captain Barbossa, long believed to be dead, ha...   \n",
       "2  A cryptic message from Bond’s past sends him o...   \n",
       "3  Following the death of District Attorney Harve...   \n",
       "4  John Carter is a war-weary, former military ca...   \n",
       "\n",
       "                                          genres  \\\n",
       "0  [Action, Adventure, Fantasy, Science Fiction]   \n",
       "1                   [Adventure, Fantasy, Action]   \n",
       "2                     [Action, Adventure, Crime]   \n",
       "3               [Action, Crime, Drama, Thriller]   \n",
       "4           [Action, Adventure, Science Fiction]   \n",
       "\n",
       "                                            keywords  \\\n",
       "0  [culture clash, future, space war, space colon...   \n",
       "1  [ocean, drug abuse, exotic island, east india ...   \n",
       "2  [spy, based on novel, secret agent, sequel, mi...   \n",
       "3  [dc comics, crime fighter, terrorist, secret i...   \n",
       "4  [based on novel, mars, medallion, space travel...   \n",
       "\n",
       "                                               cast  \\\n",
       "0  [Sam Worthington, Zoe Saldana, Sigourney Weaver]   \n",
       "1     [Johnny Depp, Orlando Bloom, Keira Knightley]   \n",
       "2      [Daniel Craig, Christoph Waltz, Léa Seydoux]   \n",
       "3      [Christian Bale, Michael Caine, Gary Oldman]   \n",
       "4    [Taylor Kitsch, Lynn Collins, Samantha Morton]   \n",
       "\n",
       "                                                crew  \n",
       "0  [{\"credit_id\": \"52fe48009251416c750aca23\", \"de...  \n",
       "1  [{\"credit_id\": \"52fe4232c3a36847f800b579\", \"de...  \n",
       "2  [{\"credit_id\": \"54805967c3a36829b5002c41\", \"de...  \n",
       "3  [{\"credit_id\": \"52fe4781c3a36847f81398c3\", \"de...  \n",
       "4  [{\"credit_id\": \"52fe479ac3a36847f813eaa3\", \"de...  "
      ]
     },
     "execution_count": 175,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies['cast'] = movies['cast'].apply(convert_cast)\n",
    "movies.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 176,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'[{\"credit_id\": \"52fe48009251416c750aca23\", \"department\": \"Editing\", \"gender\": 0, \"id\": 1721, \"job\": \"Editor\", \"name\": \"Stephen E. Rivkin\"}, {\"credit_id\": \"539c47ecc3a36810e3001f87\", \"department\": \"Art\", \"gender\": 2, \"id\": 496, \"job\": \"Production Design\", \"name\": \"Rick Carter\"}, {\"credit_id\": \"54491c89c3a3680fb4001cf7\", \"department\": \"Sound\", \"gender\": 0, \"id\": 900, \"job\": \"Sound Designer\", \"name\": \"Christopher Boyes\"}, {\"credit_id\": \"54491cb70e0a267480001bd0\", \"department\": \"Sound\", \"gender\": 0, \"id\": 900, \"job\": \"Supervising Sound Editor\", \"name\": \"Christopher Boyes\"}, {\"credit_id\": \"539c4a4cc3a36810c9002101\", \"department\": \"Production\", \"gender\": 1, \"id\": 1262, \"job\": \"Casting\", \"name\": \"Mali Finn\"}, {\"credit_id\": \"5544ee3b925141499f0008fc\", \"department\": \"Sound\", \"gender\": 2, \"id\": 1729, \"job\": \"Original Music Composer\", \"name\": \"James Horner\"}, {\"credit_id\": \"52fe48009251416c750ac9c3\", \"department\": \"Directing\", \"gender\": 2, \"id\": 2710, \"job\": \"Director\", \"name\": \"James Cameron\"}, {\"credit_id\": \"52fe48009251416c750ac9d9\", \"department\": \"Writing\", \"gender\": 2, \"id\": 2710, \"job\": \"Writer\", \"name\": \"James Cameron\"}, {\"credit_id\": \"52fe48009251416c750aca17\", \"department\": \"Editing\", \"gender\": 2, \"id\": 2710, \"job\": \"Editor\", \"name\": \"James Cameron\"}, {\"credit_id\": \"52fe48009251416c750aca29\", \"department\": \"Production\", \"gender\": 2, \"id\": 2710, \"job\": \"Producer\", \"name\": \"James Cameron\"}, {\"credit_id\": \"52fe48009251416c750aca3f\", \"department\": \"Writing\", \"gender\": 2, \"id\": 2710, \"job\": \"Screenplay\", \"name\": \"James Cameron\"}, {\"credit_id\": \"539c4987c3a36810ba0021a4\", \"department\": \"Art\", \"gender\": 2, \"id\": 7236, \"job\": \"Art Direction\", \"name\": \"Andrew Menzies\"}, {\"credit_id\": \"549598c3c3a3686ae9004383\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 6690, \"job\": \"Visual Effects Producer\", \"name\": \"Jill Brooks\"}, {\"credit_id\": \"52fe48009251416c750aca4b\", \"department\": \"Production\", \"gender\": 1, \"id\": 6347, \"job\": \"Casting\", \"name\": \"Margery Simkin\"}, {\"credit_id\": \"570b6f419251417da70032fe\", \"department\": \"Art\", \"gender\": 2, \"id\": 6878, \"job\": \"Supervising Art Director\", \"name\": \"Kevin Ishioka\"}, {\"credit_id\": \"5495a0fac3a3686ae9004468\", \"department\": \"Sound\", \"gender\": 0, \"id\": 6883, \"job\": \"Music Editor\", \"name\": \"Dick Bernstein\"}, {\"credit_id\": \"54959706c3a3686af3003e81\", \"department\": \"Sound\", \"gender\": 0, \"id\": 8159, \"job\": \"Sound Effects Editor\", \"name\": \"Shannon Mills\"}, {\"credit_id\": \"54491d58c3a3680fb1001ccb\", \"department\": \"Sound\", \"gender\": 0, \"id\": 8160, \"job\": \"Foley\", \"name\": \"Dennie Thorpe\"}, {\"credit_id\": \"54491d6cc3a3680fa5001b2c\", \"department\": \"Sound\", \"gender\": 0, \"id\": 8163, \"job\": \"Foley\", \"name\": \"Jana Vance\"}, {\"credit_id\": \"52fe48009251416c750aca57\", \"department\": \"Costume & Make-Up\", \"gender\": 1, \"id\": 8527, \"job\": \"Costume Design\", \"name\": \"Deborah Lynn Scott\"}, {\"credit_id\": \"52fe48009251416c750aca2f\", \"department\": \"Production\", \"gender\": 2, \"id\": 8529, \"job\": \"Producer\", \"name\": \"Jon Landau\"}, {\"credit_id\": \"539c4937c3a36810ba002194\", \"department\": \"Art\", \"gender\": 0, \"id\": 9618, \"job\": \"Art Direction\", \"name\": \"Sean Haworth\"}, {\"credit_id\": \"539c49b6c3a36810c10020e6\", \"department\": \"Art\", \"gender\": 1, \"id\": 12653, \"job\": \"Set Decoration\", \"name\": \"Kim Sinclair\"}, {\"credit_id\": \"570b6f2f9251413a0e00020d\", \"department\": \"Art\", \"gender\": 1, \"id\": 12653, \"job\": \"Supervising Art Director\", \"name\": \"Kim Sinclair\"}, {\"credit_id\": \"54491a6c0e0a26748c001b19\", \"department\": \"Art\", \"gender\": 2, \"id\": 14350, \"job\": \"Set Designer\", \"name\": \"Richard F. Mays\"}, {\"credit_id\": \"56928cf4c3a3684cff0025c4\", \"department\": \"Production\", \"gender\": 1, \"id\": 20294, \"job\": \"Executive Producer\", \"name\": \"Laeta Kalogridis\"}, {\"credit_id\": \"52fe48009251416c750aca51\", \"department\": \"Costume & Make-Up\", \"gender\": 0, \"id\": 17675, \"job\": \"Costume Design\", \"name\": \"Mayes C. Rubeo\"}, {\"credit_id\": \"52fe48009251416c750aca11\", \"department\": \"Camera\", \"gender\": 2, \"id\": 18265, \"job\": \"Director of Photography\", \"name\": \"Mauro Fiore\"}, {\"credit_id\": \"5449194d0e0a26748f001b39\", \"department\": \"Art\", \"gender\": 0, \"id\": 42281, \"job\": \"Set Designer\", \"name\": \"Scott Herbertson\"}, {\"credit_id\": \"52fe48009251416c750aca05\", \"department\": \"Crew\", \"gender\": 0, \"id\": 42288, \"job\": \"Stunts\", \"name\": \"Woody Schultz\"}, {\"credit_id\": \"5592aefb92514152de0010f5\", \"department\": \"Costume & Make-Up\", \"gender\": 0, \"id\": 29067, \"job\": \"Makeup Artist\", \"name\": \"Linda DeVetta\"}, {\"credit_id\": \"5592afa492514152de00112c\", \"department\": \"Costume & Make-Up\", \"gender\": 0, \"id\": 29067, \"job\": \"Hairstylist\", \"name\": \"Linda DeVetta\"}, {\"credit_id\": \"54959ed592514130fc002e5d\", \"department\": \"Camera\", \"gender\": 2, \"id\": 33302, \"job\": \"Camera Operator\", \"name\": \"Richard Bluck\"}, {\"credit_id\": \"539c4891c3a36810ba002147\", \"department\": \"Art\", \"gender\": 2, \"id\": 33303, \"job\": \"Art Direction\", \"name\": \"Simon Bright\"}, {\"credit_id\": \"54959c069251417a81001f3a\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 113145, \"job\": \"Visual Effects Supervisor\", \"name\": \"Richard Martin\"}, {\"credit_id\": \"54959a0dc3a3680ff5002c8d\", \"department\": \"Crew\", \"gender\": 2, \"id\": 58188, \"job\": \"Visual Effects Editor\", \"name\": \"Steve R. Moore\"}, {\"credit_id\": \"52fe48009251416c750aca1d\", \"department\": \"Editing\", \"gender\": 2, \"id\": 58871, \"job\": \"Editor\", \"name\": \"John Refoua\"}, {\"credit_id\": \"54491a4dc3a3680fc30018ca\", \"department\": \"Art\", \"gender\": 0, \"id\": 92359, \"job\": \"Set Designer\", \"name\": \"Karl J. Martin\"}, {\"credit_id\": \"52fe48009251416c750aca35\", \"department\": \"Camera\", \"gender\": 1, \"id\": 72201, \"job\": \"Director of Photography\", \"name\": \"Chiling Lin\"}, {\"credit_id\": \"52fe48009251416c750ac9ff\", \"department\": \"Crew\", \"gender\": 0, \"id\": 89714, \"job\": \"Stunts\", \"name\": \"Ilram Choi\"}, {\"credit_id\": \"54959c529251416e2b004394\", \"department\": \"Visual Effects\", \"gender\": 2, \"id\": 93214, \"job\": \"Visual Effects Supervisor\", \"name\": \"Steven Quale\"}, {\"credit_id\": \"54491edf0e0a267489001c37\", \"department\": \"Crew\", \"gender\": 1, \"id\": 122607, \"job\": \"Dialect Coach\", \"name\": \"Carla Meyer\"}, {\"credit_id\": \"539c485bc3a368653d001a3a\", \"department\": \"Art\", \"gender\": 2, \"id\": 132585, \"job\": \"Art Direction\", \"name\": \"Nick Bassett\"}, {\"credit_id\": \"539c4903c3a368653d001a74\", \"department\": \"Art\", \"gender\": 0, \"id\": 132596, \"job\": \"Art Direction\", \"name\": \"Jill Cormack\"}, {\"credit_id\": \"539c4967c3a368653d001a94\", \"department\": \"Art\", \"gender\": 0, \"id\": 132604, \"job\": \"Art Direction\", \"name\": \"Andy McLaren\"}, {\"credit_id\": \"52fe48009251416c750aca45\", \"department\": \"Crew\", \"gender\": 0, \"id\": 236696, \"job\": \"Motion Capture Artist\", \"name\": \"Terry Notary\"}, {\"credit_id\": \"54959e02c3a3680fc60027d2\", \"department\": \"Crew\", \"gender\": 2, \"id\": 956198, \"job\": \"Stunt Coordinator\", \"name\": \"Garrett Warren\"}, {\"credit_id\": \"54959ca3c3a3686ae300438c\", \"department\": \"Visual Effects\", \"gender\": 2, \"id\": 957874, \"job\": \"Visual Effects Supervisor\", \"name\": \"Jonathan Rothbart\"}, {\"credit_id\": \"570b6f519251412c74001b2f\", \"department\": \"Art\", \"gender\": 0, \"id\": 957889, \"job\": \"Supervising Art Director\", \"name\": \"Stefan Dechant\"}, {\"credit_id\": \"570b6f62c3a3680b77007460\", \"department\": \"Art\", \"gender\": 2, \"id\": 959555, \"job\": \"Supervising Art Director\", \"name\": \"Todd Cherniawsky\"}, {\"credit_id\": \"539c4a3ac3a36810da0021cc\", \"department\": \"Production\", \"gender\": 0, \"id\": 1016177, \"job\": \"Casting\", \"name\": \"Miranda Rivers\"}, {\"credit_id\": \"539c482cc3a36810c1002062\", \"department\": \"Art\", \"gender\": 0, \"id\": 1032536, \"job\": \"Production Design\", \"name\": \"Robert Stromberg\"}, {\"credit_id\": \"539c4b65c3a36810c9002125\", \"department\": \"Costume & Make-Up\", \"gender\": 2, \"id\": 1071680, \"job\": \"Costume Design\", \"name\": \"John Harding\"}, {\"credit_id\": \"54959e6692514130fc002e4e\", \"department\": \"Camera\", \"gender\": 0, \"id\": 1177364, \"job\": \"Steadicam Operator\", \"name\": \"Roberto De Angelis\"}, {\"credit_id\": \"539c49f1c3a368653d001aac\", \"department\": \"Costume & Make-Up\", \"gender\": 2, \"id\": 1202850, \"job\": \"Makeup Department Head\", \"name\": \"Mike Smithson\"}, {\"credit_id\": \"5495999ec3a3686ae100460c\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1204668, \"job\": \"Visual Effects Producer\", \"name\": \"Alain Lalanne\"}, {\"credit_id\": \"54959cdfc3a3681153002729\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1206410, \"job\": \"Visual Effects Supervisor\", \"name\": \"Lucas Salton\"}, {\"credit_id\": \"549596239251417a81001eae\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1234266, \"job\": \"Post Production Supervisor\", \"name\": \"Janace Tashjian\"}, {\"credit_id\": \"54959c859251416e1e003efe\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1271932, \"job\": \"Visual Effects Supervisor\", \"name\": \"Stephen Rosenbaum\"}, {\"credit_id\": \"5592af28c3a368775a00105f\", \"department\": \"Costume & Make-Up\", \"gender\": 0, \"id\": 1310064, \"job\": \"Makeup Artist\", \"name\": \"Frankie Karena\"}, {\"credit_id\": \"539c4adfc3a36810e300203b\", \"department\": \"Costume & Make-Up\", \"gender\": 1, \"id\": 1319844, \"job\": \"Costume Supervisor\", \"name\": \"Lisa Lovaas\"}, {\"credit_id\": \"54959b579251416e2b004371\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1327028, \"job\": \"Visual Effects Supervisor\", \"name\": \"Jonathan Fawkner\"}, {\"credit_id\": \"539c48a7c3a36810b5001fa7\", \"department\": \"Art\", \"gender\": 0, \"id\": 1330561, \"job\": \"Art Direction\", \"name\": \"Robert Bavin\"}, {\"credit_id\": \"539c4a71c3a36810da0021e0\", \"department\": \"Costume & Make-Up\", \"gender\": 0, \"id\": 1330567, \"job\": \"Costume Supervisor\", \"name\": \"Anthony Almaraz\"}, {\"credit_id\": \"539c4a8ac3a36810ba0021e4\", \"department\": \"Costume & Make-Up\", \"gender\": 0, \"id\": 1330570, \"job\": \"Costume Supervisor\", \"name\": \"Carolyn M. Fenton\"}, {\"credit_id\": \"539c4ab6c3a36810da0021f0\", \"department\": \"Costume & Make-Up\", \"gender\": 0, \"id\": 1330574, \"job\": \"Costume Supervisor\", \"name\": \"Beth Koenigsberg\"}, {\"credit_id\": \"54491ab70e0a267480001ba2\", \"department\": \"Art\", \"gender\": 0, \"id\": 1336191, \"job\": \"Set Designer\", \"name\": \"Sam Page\"}, {\"credit_id\": \"544919d9c3a3680fc30018bd\", \"department\": \"Art\", \"gender\": 0, \"id\": 1339441, \"job\": \"Set Designer\", \"name\": \"Tex Kadonaga\"}, {\"credit_id\": \"54491cf50e0a267483001b0c\", \"department\": \"Editing\", \"gender\": 0, \"id\": 1352422, \"job\": \"Dialogue Editor\", \"name\": \"Kim Foscato\"}, {\"credit_id\": \"544919f40e0a26748c001b09\", \"department\": \"Art\", \"gender\": 0, \"id\": 1352962, \"job\": \"Set Designer\", \"name\": \"Tammy S. Lee\"}, {\"credit_id\": \"5495a115c3a3680ff5002d71\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1357070, \"job\": \"Transportation Coordinator\", \"name\": \"Denny Caira\"}, {\"credit_id\": \"5495a12f92514130fc002e94\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1357071, \"job\": \"Transportation Coordinator\", \"name\": \"James Waitkus\"}, {\"credit_id\": \"5495976fc3a36811530026b0\", \"department\": \"Sound\", \"gender\": 0, \"id\": 1360103, \"job\": \"Supervising Sound Editor\", \"name\": \"Addison Teague\"}, {\"credit_id\": \"54491837c3a3680fb1001c5a\", \"department\": \"Art\", \"gender\": 2, \"id\": 1376887, \"job\": \"Set Designer\", \"name\": \"C. Scott Baker\"}, {\"credit_id\": \"54491878c3a3680fb4001c9d\", \"department\": \"Art\", \"gender\": 0, \"id\": 1376888, \"job\": \"Set Designer\", \"name\": \"Luke Caska\"}, {\"credit_id\": \"544918dac3a3680fa5001ae0\", \"department\": \"Art\", \"gender\": 0, \"id\": 1376889, \"job\": \"Set Designer\", \"name\": \"David Chow\"}, {\"credit_id\": \"544919110e0a267486001b68\", \"department\": \"Art\", \"gender\": 0, \"id\": 1376890, \"job\": \"Set Designer\", \"name\": \"Jonathan Dyer\"}, {\"credit_id\": \"54491967c3a3680faa001b5e\", \"department\": \"Art\", \"gender\": 0, \"id\": 1376891, \"job\": \"Set Designer\", \"name\": \"Joseph Hiura\"}, {\"credit_id\": \"54491997c3a3680fb1001c8a\", \"department\": \"Art\", \"gender\": 0, \"id\": 1376892, \"job\": \"Art Department Coordinator\", \"name\": \"Rebecca Jellie\"}, {\"credit_id\": \"544919ba0e0a26748f001b42\", \"department\": \"Art\", \"gender\": 0, \"id\": 1376893, \"job\": \"Set Designer\", \"name\": \"Robert Andrew Johnson\"}, {\"credit_id\": \"54491b1dc3a3680faa001b8c\", \"department\": \"Art\", \"gender\": 0, \"id\": 1376895, \"job\": \"Assistant Art Director\", \"name\": \"Mike Stassi\"}, {\"credit_id\": \"54491b79c3a3680fbb001826\", \"department\": \"Art\", \"gender\": 0, \"id\": 1376897, \"job\": \"Construction Coordinator\", \"name\": \"John Villarino\"}, {\"credit_id\": \"54491baec3a3680fb4001ce6\", \"department\": \"Art\", \"gender\": 2, \"id\": 1376898, \"job\": \"Assistant Art Director\", \"name\": \"Jeffrey Wisniewski\"}, {\"credit_id\": \"54491d2fc3a3680fb4001d07\", \"department\": \"Editing\", \"gender\": 0, \"id\": 1376899, \"job\": \"Dialogue Editor\", \"name\": \"Cheryl Nardi\"}, {\"credit_id\": \"54491d86c3a3680fa5001b2f\", \"department\": \"Editing\", \"gender\": 0, \"id\": 1376901, \"job\": \"Dialogue Editor\", \"name\": \"Marshall Winn\"}, {\"credit_id\": \"54491d9dc3a3680faa001bb0\", \"department\": \"Sound\", \"gender\": 0, \"id\": 1376902, \"job\": \"Supervising Sound Editor\", \"name\": \"Gwendolyn Yates Whittle\"}, {\"credit_id\": \"54491dc10e0a267486001bce\", \"department\": \"Sound\", \"gender\": 0, \"id\": 1376903, \"job\": \"Sound Re-Recording Mixer\", \"name\": \"William Stein\"}, {\"credit_id\": \"54491f500e0a26747c001c07\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1376909, \"job\": \"Choreographer\", \"name\": \"Lula Washington\"}, {\"credit_id\": \"549599239251412c4e002a2e\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1391692, \"job\": \"Visual Effects Producer\", \"name\": \"Chris Del Conte\"}, {\"credit_id\": \"54959d54c3a36831b8001d9a\", \"department\": \"Visual Effects\", \"gender\": 2, \"id\": 1391695, \"job\": \"Visual Effects Supervisor\", \"name\": \"R. Christopher White\"}, {\"credit_id\": \"54959bdf9251412c4e002a66\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1394070, \"job\": \"Visual Effects Supervisor\", \"name\": \"Dan Lemmon\"}, {\"credit_id\": \"5495971d92514132ed002922\", \"department\": \"Sound\", \"gender\": 0, \"id\": 1394129, \"job\": \"Sound Effects Editor\", \"name\": \"Tim Nielsen\"}, {\"credit_id\": \"5592b25792514152cc0011aa\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1394286, \"job\": \"CG Supervisor\", \"name\": \"Michael Mulholland\"}, {\"credit_id\": \"54959a329251416e2b004355\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1394750, \"job\": \"Visual Effects Editor\", \"name\": \"Thomas Nittmann\"}, {\"credit_id\": \"54959d6dc3a3686ae9004401\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1394755, \"job\": \"Visual Effects Supervisor\", \"name\": \"Edson Williams\"}, {\"credit_id\": \"5495a08fc3a3686ae300441c\", \"department\": \"Editing\", \"gender\": 0, \"id\": 1394953, \"job\": \"Digital Intermediate\", \"name\": \"Christine Carr\"}, {\"credit_id\": \"55402d659251413d6d000249\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1395269, \"job\": \"Visual Effects Supervisor\", \"name\": \"John Bruno\"}, {\"credit_id\": \"54959e7b9251416e1e003f3e\", \"department\": \"Camera\", \"gender\": 0, \"id\": 1398970, \"job\": \"Steadicam Operator\", \"name\": \"David Emmerichs\"}, {\"credit_id\": \"54959734c3a3686ae10045e0\", \"department\": \"Sound\", \"gender\": 0, \"id\": 1400906, \"job\": \"Sound Effects Editor\", \"name\": \"Christopher Scarabosio\"}, {\"credit_id\": \"549595dd92514130fc002d79\", \"department\": \"Production\", \"gender\": 0, \"id\": 1401784, \"job\": \"Production Supervisor\", \"name\": \"Jennifer Teves\"}, {\"credit_id\": \"549596009251413af70028cc\", \"department\": \"Production\", \"gender\": 0, \"id\": 1401785, \"job\": \"Production Manager\", \"name\": \"Brigitte Yorke\"}, {\"credit_id\": \"549596e892514130fc002d99\", \"department\": \"Sound\", \"gender\": 0, \"id\": 1401786, \"job\": \"Sound Effects Editor\", \"name\": \"Ken Fischer\"}, {\"credit_id\": \"549598229251412c4e002a1c\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1401787, \"job\": \"Special Effects Coordinator\", \"name\": \"Iain Hutton\"}, {\"credit_id\": \"549598349251416e2b00432b\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1401788, \"job\": \"Special Effects Coordinator\", \"name\": \"Steve Ingram\"}, {\"credit_id\": \"54959905c3a3686ae3004324\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1401789, \"job\": \"Visual Effects Producer\", \"name\": \"Joyce Cox\"}, {\"credit_id\": \"5495994b92514132ed002951\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1401790, \"job\": \"Visual Effects Producer\", \"name\": \"Jenny Foster\"}, {\"credit_id\": \"549599cbc3a3686ae1004613\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1401791, \"job\": \"Visual Effects Editor\", \"name\": \"Christopher Marino\"}, {\"credit_id\": \"549599f2c3a3686ae100461e\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1401792, \"job\": \"Visual Effects Editor\", \"name\": \"Jim Milton\"}, {\"credit_id\": \"54959a51c3a3686af3003eb5\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1401793, \"job\": \"Visual Effects Producer\", \"name\": \"Cyndi Ochs\"}, {\"credit_id\": \"54959a7cc3a36811530026f4\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1401794, \"job\": \"Visual Effects Editor\", \"name\": \"Lucas Putnam\"}, {\"credit_id\": \"54959b91c3a3680ff5002cb4\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1401795, \"job\": \"Visual Effects Supervisor\", \"name\": \"Anthony \\'Max\\' Ivins\"}, {\"credit_id\": \"54959bb69251412c4e002a5f\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1401796, \"job\": \"Visual Effects Supervisor\", \"name\": \"John Knoll\"}, {\"credit_id\": \"54959cbbc3a3686ae3004391\", \"department\": \"Visual Effects\", \"gender\": 2, \"id\": 1401799, \"job\": \"Visual Effects Supervisor\", \"name\": \"Eric Saindon\"}, {\"credit_id\": \"54959d06c3a3686ae90043f6\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1401800, \"job\": \"Visual Effects Supervisor\", \"name\": \"Wayne Stables\"}, {\"credit_id\": \"54959d259251416e1e003f11\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1401801, \"job\": \"Visual Effects Supervisor\", \"name\": \"David Stinnett\"}, {\"credit_id\": \"54959db49251413af7002975\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1401803, \"job\": \"Visual Effects Supervisor\", \"name\": \"Guy Williams\"}, {\"credit_id\": \"54959de4c3a3681153002750\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1401804, \"job\": \"Stunt Coordinator\", \"name\": \"Stuart Thorp\"}, {\"credit_id\": \"54959ef2c3a3680fc60027f2\", \"department\": \"Lighting\", \"gender\": 0, \"id\": 1401805, \"job\": \"Best Boy Electric\", \"name\": \"Giles Coburn\"}, {\"credit_id\": \"54959f07c3a3680fc60027f9\", \"department\": \"Camera\", \"gender\": 2, \"id\": 1401806, \"job\": \"Still Photographer\", \"name\": \"Mark Fellman\"}, {\"credit_id\": \"54959f47c3a3681153002774\", \"department\": \"Lighting\", \"gender\": 0, \"id\": 1401807, \"job\": \"Lighting Technician\", \"name\": \"Scott Sprague\"}, {\"credit_id\": \"54959f8cc3a36831b8001df2\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1401808, \"job\": \"Animation Director\", \"name\": \"Jeremy Hollobon\"}, {\"credit_id\": \"54959fa0c3a36831b8001dfb\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1401809, \"job\": \"Animation Director\", \"name\": \"Orlando Meunier\"}, {\"credit_id\": \"54959fb6c3a3686af3003f54\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1401810, \"job\": \"Animation Director\", \"name\": \"Taisuke Tanimura\"}, {\"credit_id\": \"54959fd2c3a36831b8001e02\", \"department\": \"Costume & Make-Up\", \"gender\": 0, \"id\": 1401812, \"job\": \"Set Costumer\", \"name\": \"Lilia Mishel Acevedo\"}, {\"credit_id\": \"54959ff9c3a3686ae300440c\", \"department\": \"Costume & Make-Up\", \"gender\": 0, \"id\": 1401814, \"job\": \"Set Costumer\", \"name\": \"Alejandro M. Hernandez\"}, {\"credit_id\": \"5495a0ddc3a3686ae10046fe\", \"department\": \"Editing\", \"gender\": 0, \"id\": 1401815, \"job\": \"Digital Intermediate\", \"name\": \"Marvin Hall\"}, {\"credit_id\": \"5495a1f7c3a3686ae3004443\", \"department\": \"Production\", \"gender\": 0, \"id\": 1401816, \"job\": \"Publicist\", \"name\": \"Judy Alley\"}, {\"credit_id\": \"5592b29fc3a36869d100002f\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1418381, \"job\": \"CG Supervisor\", \"name\": \"Mike Perry\"}, {\"credit_id\": \"5592b23a9251415df8001081\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1426854, \"job\": \"CG Supervisor\", \"name\": \"Andrew Morley\"}, {\"credit_id\": \"55491e1192514104c40002d8\", \"department\": \"Art\", \"gender\": 0, \"id\": 1438901, \"job\": \"Conceptual Design\", \"name\": \"Seth Engstrom\"}, {\"credit_id\": \"5525d5809251417276002b06\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1447362, \"job\": \"Visual Effects Art Director\", \"name\": \"Eric Oliver\"}, {\"credit_id\": \"554427ca925141586500312a\", \"department\": \"Visual Effects\", \"gender\": 0, \"id\": 1447503, \"job\": \"Modeling\", \"name\": \"Matsune Suzuki\"}, {\"credit_id\": \"551906889251415aab001c88\", \"department\": \"Art\", \"gender\": 0, \"id\": 1447524, \"job\": \"Art Department Manager\", \"name\": \"Paul Tobin\"}, {\"credit_id\": \"5592af8492514152cc0010de\", \"department\": \"Costume & Make-Up\", \"gender\": 0, \"id\": 1452643, \"job\": \"Hairstylist\", \"name\": \"Roxane Griffin\"}, {\"credit_id\": \"553d3c109251415852001318\", \"department\": \"Lighting\", \"gender\": 0, \"id\": 1453938, \"job\": \"Lighting Artist\", \"name\": \"Arun Ram-Mohan\"}, {\"credit_id\": \"5592af4692514152d5001355\", \"department\": \"Costume & Make-Up\", \"gender\": 0, \"id\": 1457305, \"job\": \"Makeup Artist\", \"name\": \"Georgia Lockhart-Adams\"}, {\"credit_id\": \"5592b2eac3a36877470012a5\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1466035, \"job\": \"CG Supervisor\", \"name\": \"Thrain Shadbolt\"}, {\"credit_id\": \"5592b032c3a36877450015f1\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1483220, \"job\": \"CG Supervisor\", \"name\": \"Brad Alexander\"}, {\"credit_id\": \"5592b05592514152d80012f6\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1483221, \"job\": \"CG Supervisor\", \"name\": \"Shadi Almassizadeh\"}, {\"credit_id\": \"5592b090c3a36877570010b5\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1483222, \"job\": \"CG Supervisor\", \"name\": \"Simon Clutterbuck\"}, {\"credit_id\": \"5592b0dbc3a368774b00112c\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1483223, \"job\": \"CG Supervisor\", \"name\": \"Graeme Demmocks\"}, {\"credit_id\": \"5592b0fe92514152db0010c1\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1483224, \"job\": \"CG Supervisor\", \"name\": \"Adrian Fernandes\"}, {\"credit_id\": \"5592b11f9251415df8001059\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1483225, \"job\": \"CG Supervisor\", \"name\": \"Mitch Gates\"}, {\"credit_id\": \"5592b15dc3a3687745001645\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1483226, \"job\": \"CG Supervisor\", \"name\": \"Jerry Kung\"}, {\"credit_id\": \"5592b18e925141645a0004ae\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1483227, \"job\": \"CG Supervisor\", \"name\": \"Andy Lomas\"}, {\"credit_id\": \"5592b1bfc3a368775d0010e7\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1483228, \"job\": \"CG Supervisor\", \"name\": \"Sebastian Marino\"}, {\"credit_id\": \"5592b2049251415df8001078\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1483229, \"job\": \"CG Supervisor\", \"name\": \"Matthias Menz\"}, {\"credit_id\": \"5592b27b92514152d800136a\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1483230, \"job\": \"CG Supervisor\", \"name\": \"Sergei Nevshupov\"}, {\"credit_id\": \"5592b2c3c3a36869e800003c\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1483231, \"job\": \"CG Supervisor\", \"name\": \"Philippe Rebours\"}, {\"credit_id\": \"5592b317c3a36877470012af\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1483232, \"job\": \"CG Supervisor\", \"name\": \"Michael Takarangi\"}, {\"credit_id\": \"5592b345c3a36877470012bb\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1483233, \"job\": \"CG Supervisor\", \"name\": \"David Weitzberg\"}, {\"credit_id\": \"5592b37cc3a368775100113b\", \"department\": \"Crew\", \"gender\": 0, \"id\": 1483234, \"job\": \"CG Supervisor\", \"name\": \"Ben White\"}, {\"credit_id\": \"573c8e2f9251413f5d000094\", \"department\": \"Crew\", \"gender\": 1, \"id\": 1621932, \"job\": \"Stunts\", \"name\": \"Min Windle\"}]'"
      ]
     },
     "execution_count": 176,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# handle crew\n",
    "\n",
    "movies.iloc[0]['crew']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 177,
   "metadata": {},
   "outputs": [],
   "source": [
    "def fetch_director(text):\n",
    "    L = []\n",
    "    for i in ast.literal_eval(text):\n",
    "        if i['job'] == 'Director':\n",
    "            L.append(i['name'])\n",
    "            break\n",
    "    return L"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 178,
   "metadata": {},
   "outputs": [],
   "source": [
    "movies['crew'] = movies['crew'].apply(fetch_director)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 179,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>movie_id</th>\n",
       "      <th>title</th>\n",
       "      <th>overview</th>\n",
       "      <th>genres</th>\n",
       "      <th>keywords</th>\n",
       "      <th>cast</th>\n",
       "      <th>crew</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>19995</td>\n",
       "      <td>Avatar</td>\n",
       "      <td>In the 22nd century, a paraplegic Marine is di...</td>\n",
       "      <td>[Action, Adventure, Fantasy, Science Fiction]</td>\n",
       "      <td>[culture clash, future, space war, space colon...</td>\n",
       "      <td>[Sam Worthington, Zoe Saldana, Sigourney Weaver]</td>\n",
       "      <td>[James Cameron]</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>285</td>\n",
       "      <td>Pirates of the Caribbean: At World's End</td>\n",
       "      <td>Captain Barbossa, long believed to be dead, ha...</td>\n",
       "      <td>[Adventure, Fantasy, Action]</td>\n",
       "      <td>[ocean, drug abuse, exotic island, east india ...</td>\n",
       "      <td>[Johnny Depp, Orlando Bloom, Keira Knightley]</td>\n",
       "      <td>[Gore Verbinski]</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>206647</td>\n",
       "      <td>Spectre</td>\n",
       "      <td>A cryptic message from Bond’s past sends him o...</td>\n",
       "      <td>[Action, Adventure, Crime]</td>\n",
       "      <td>[spy, based on novel, secret agent, sequel, mi...</td>\n",
       "      <td>[Daniel Craig, Christoph Waltz, Léa Seydoux]</td>\n",
       "      <td>[Sam Mendes]</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>49026</td>\n",
       "      <td>The Dark Knight Rises</td>\n",
       "      <td>Following the death of District Attorney Harve...</td>\n",
       "      <td>[Action, Crime, Drama, Thriller]</td>\n",
       "      <td>[dc comics, crime fighter, terrorist, secret i...</td>\n",
       "      <td>[Christian Bale, Michael Caine, Gary Oldman]</td>\n",
       "      <td>[Christopher Nolan]</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>49529</td>\n",
       "      <td>John Carter</td>\n",
       "      <td>John Carter is a war-weary, former military ca...</td>\n",
       "      <td>[Action, Adventure, Science Fiction]</td>\n",
       "      <td>[based on novel, mars, medallion, space travel...</td>\n",
       "      <td>[Taylor Kitsch, Lynn Collins, Samantha Morton]</td>\n",
       "      <td>[Andrew Stanton]</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   movie_id                                     title  \\\n",
       "0     19995                                    Avatar   \n",
       "1       285  Pirates of the Caribbean: At World's End   \n",
       "2    206647                                   Spectre   \n",
       "3     49026                     The Dark Knight Rises   \n",
       "4     49529                               John Carter   \n",
       "\n",
       "                                            overview  \\\n",
       "0  In the 22nd century, a paraplegic Marine is di...   \n",
       "1  Captain Barbossa, long believed to be dead, ha...   \n",
       "2  A cryptic message from Bond’s past sends him o...   \n",
       "3  Following the death of District Attorney Harve...   \n",
       "4  John Carter is a war-weary, former military ca...   \n",
       "\n",
       "                                          genres  \\\n",
       "0  [Action, Adventure, Fantasy, Science Fiction]   \n",
       "1                   [Adventure, Fantasy, Action]   \n",
       "2                     [Action, Adventure, Crime]   \n",
       "3               [Action, Crime, Drama, Thriller]   \n",
       "4           [Action, Adventure, Science Fiction]   \n",
       "\n",
       "                                            keywords  \\\n",
       "0  [culture clash, future, space war, space colon...   \n",
       "1  [ocean, drug abuse, exotic island, east india ...   \n",
       "2  [spy, based on novel, secret agent, sequel, mi...   \n",
       "3  [dc comics, crime fighter, terrorist, secret i...   \n",
       "4  [based on novel, mars, medallion, space travel...   \n",
       "\n",
       "                                               cast                 crew  \n",
       "0  [Sam Worthington, Zoe Saldana, Sigourney Weaver]      [James Cameron]  \n",
       "1     [Johnny Depp, Orlando Bloom, Keira Knightley]     [Gore Verbinski]  \n",
       "2      [Daniel Craig, Christoph Waltz, Léa Seydoux]         [Sam Mendes]  \n",
       "3      [Christian Bale, Michael Caine, Gary Oldman]  [Christopher Nolan]  \n",
       "4    [Taylor Kitsch, Lynn Collins, Samantha Morton]     [Andrew Stanton]  "
      ]
     },
     "execution_count": 179,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 180,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.'"
      ]
     },
     "execution_count": 180,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# handle overview (converting to list)\n",
    "\n",
    "movies.iloc[0]['overview']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 181,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>movie_id</th>\n",
       "      <th>title</th>\n",
       "      <th>overview</th>\n",
       "      <th>genres</th>\n",
       "      <th>keywords</th>\n",
       "      <th>cast</th>\n",
       "      <th>crew</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>2337</th>\n",
       "      <td>10934</td>\n",
       "      <td>Under the Tuscan Sun</td>\n",
       "      <td>[After, a, rough, divoce,, Frances,, a, 35, ye...</td>\n",
       "      <td>[Comedy, Drama, Romance]</td>\n",
       "      <td>[depression, toscana, recreation, author, divo...</td>\n",
       "      <td>[Diane Lane, Sandra Oh, Lindsay Duncan]</td>\n",
       "      <td>[Audrey Wells]</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2948</th>\n",
       "      <td>11184</td>\n",
       "      <td>Kinsey</td>\n",
       "      <td>[Kinsey, is, a, portrait, of, researcher, Alfr...</td>\n",
       "      <td>[Drama]</td>\n",
       "      <td>[free love, sex, sexuality, indiana, professor...</td>\n",
       "      <td>[Liam Neeson, Laura Linney, Chris O'Donnell]</td>\n",
       "      <td>[Bill Condon]</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1432</th>\n",
       "      <td>14175</td>\n",
       "      <td>Valiant</td>\n",
       "      <td>[The, animated, comedy, tells, the, story, of,...</td>\n",
       "      <td>[Animation, Family, Adventure]</td>\n",
       "      <td>[animation, animal, 3d]</td>\n",
       "      <td>[Ewan McGregor, Ricky Gervais, Tim Curry]</td>\n",
       "      <td>[Gary Chapman]</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3364</th>\n",
       "      <td>22314</td>\n",
       "      <td>In Too Deep</td>\n",
       "      <td>[A, fearless, cop, is, taking, on, a, ruthless...</td>\n",
       "      <td>[Drama, Action, Thriller, Crime]</td>\n",
       "      <td>[]</td>\n",
       "      <td>[Omar Epps, LL Cool J, Nia Long]</td>\n",
       "      <td>[Michael Rymer]</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "      movie_id                 title  \\\n",
       "2337     10934  Under the Tuscan Sun   \n",
       "2948     11184                Kinsey   \n",
       "1432     14175               Valiant   \n",
       "3364     22314           In Too Deep   \n",
       "\n",
       "                                               overview  \\\n",
       "2337  [After, a, rough, divoce,, Frances,, a, 35, ye...   \n",
       "2948  [Kinsey, is, a, portrait, of, researcher, Alfr...   \n",
       "1432  [The, animated, comedy, tells, the, story, of,...   \n",
       "3364  [A, fearless, cop, is, taking, on, a, ruthless...   \n",
       "\n",
       "                                genres  \\\n",
       "2337          [Comedy, Drama, Romance]   \n",
       "2948                           [Drama]   \n",
       "1432    [Animation, Family, Adventure]   \n",
       "3364  [Drama, Action, Thriller, Crime]   \n",
       "\n",
       "                                               keywords  \\\n",
       "2337  [depression, toscana, recreation, author, divo...   \n",
       "2948  [free love, sex, sexuality, indiana, professor...   \n",
       "1432                            [animation, animal, 3d]   \n",
       "3364                                                 []   \n",
       "\n",
       "                                              cast             crew  \n",
       "2337       [Diane Lane, Sandra Oh, Lindsay Duncan]   [Audrey Wells]  \n",
       "2948  [Liam Neeson, Laura Linney, Chris O'Donnell]    [Bill Condon]  \n",
       "1432     [Ewan McGregor, Ricky Gervais, Tim Curry]   [Gary Chapman]  \n",
       "3364              [Omar Epps, LL Cool J, Nia Long]  [Michael Rymer]  "
      ]
     },
     "execution_count": 181,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies['overview'] = movies['overview'].apply(lambda x:x.split())\n",
    "movies.sample(4)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 182,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['In',\n",
       " 'the',\n",
       " '22nd',\n",
       " 'century,',\n",
       " 'a',\n",
       " 'paraplegic',\n",
       " 'Marine',\n",
       " 'is',\n",
       " 'dispatched',\n",
       " 'to',\n",
       " 'the',\n",
       " 'moon',\n",
       " 'Pandora',\n",
       " 'on',\n",
       " 'a',\n",
       " 'unique',\n",
       " 'mission,',\n",
       " 'but',\n",
       " 'becomes',\n",
       " 'torn',\n",
       " 'between',\n",
       " 'following',\n",
       " 'orders',\n",
       " 'and',\n",
       " 'protecting',\n",
       " 'an',\n",
       " 'alien',\n",
       " 'civilization.']"
      ]
     },
     "execution_count": 182,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.iloc[0]['overview']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 183,
   "metadata": {},
   "outputs": [],
   "source": [
    "# now removing space like that \n",
    "'Anna Kendrick'\n",
    "'AnnaKendrick'\n",
    "\n",
    "def remove_space(L):\n",
    "    L1 = []\n",
    "    for i in L:\n",
    "        L1.append(i.replace(\" \",\"\"))\n",
    "    return L1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 184,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "movies['cast'] = movies['cast'].apply(remove_space)\n",
    "movies['crew'] = movies['crew'].apply(remove_space)\n",
    "movies['genres'] = movies['genres'].apply(remove_space)\n",
    "movies['keywords'] = movies['keywords'].apply(remove_space)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 185,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>movie_id</th>\n",
       "      <th>title</th>\n",
       "      <th>overview</th>\n",
       "      <th>genres</th>\n",
       "      <th>keywords</th>\n",
       "      <th>cast</th>\n",
       "      <th>crew</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>19995</td>\n",
       "      <td>Avatar</td>\n",
       "      <td>[In, the, 22nd, century,, a, paraplegic, Marin...</td>\n",
       "      <td>[Action, Adventure, Fantasy, ScienceFiction]</td>\n",
       "      <td>[cultureclash, future, spacewar, spacecolony, ...</td>\n",
       "      <td>[SamWorthington, ZoeSaldana, SigourneyWeaver]</td>\n",
       "      <td>[JamesCameron]</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>285</td>\n",
       "      <td>Pirates of the Caribbean: At World's End</td>\n",
       "      <td>[Captain, Barbossa,, long, believed, to, be, d...</td>\n",
       "      <td>[Adventure, Fantasy, Action]</td>\n",
       "      <td>[ocean, drugabuse, exoticisland, eastindiatrad...</td>\n",
       "      <td>[JohnnyDepp, OrlandoBloom, KeiraKnightley]</td>\n",
       "      <td>[GoreVerbinski]</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>206647</td>\n",
       "      <td>Spectre</td>\n",
       "      <td>[A, cryptic, message, from, Bond’s, past, send...</td>\n",
       "      <td>[Action, Adventure, Crime]</td>\n",
       "      <td>[spy, basedonnovel, secretagent, sequel, mi6, ...</td>\n",
       "      <td>[DanielCraig, ChristophWaltz, LéaSeydoux]</td>\n",
       "      <td>[SamMendes]</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>49026</td>\n",
       "      <td>The Dark Knight Rises</td>\n",
       "      <td>[Following, the, death, of, District, Attorney...</td>\n",
       "      <td>[Action, Crime, Drama, Thriller]</td>\n",
       "      <td>[dccomics, crimefighter, terrorist, secretiden...</td>\n",
       "      <td>[ChristianBale, MichaelCaine, GaryOldman]</td>\n",
       "      <td>[ChristopherNolan]</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>49529</td>\n",
       "      <td>John Carter</td>\n",
       "      <td>[John, Carter, is, a, war-weary,, former, mili...</td>\n",
       "      <td>[Action, Adventure, ScienceFiction]</td>\n",
       "      <td>[basedonnovel, mars, medallion, spacetravel, p...</td>\n",
       "      <td>[TaylorKitsch, LynnCollins, SamanthaMorton]</td>\n",
       "      <td>[AndrewStanton]</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   movie_id                                     title  \\\n",
       "0     19995                                    Avatar   \n",
       "1       285  Pirates of the Caribbean: At World's End   \n",
       "2    206647                                   Spectre   \n",
       "3     49026                     The Dark Knight Rises   \n",
       "4     49529                               John Carter   \n",
       "\n",
       "                                            overview  \\\n",
       "0  [In, the, 22nd, century,, a, paraplegic, Marin...   \n",
       "1  [Captain, Barbossa,, long, believed, to, be, d...   \n",
       "2  [A, cryptic, message, from, Bond’s, past, send...   \n",
       "3  [Following, the, death, of, District, Attorney...   \n",
       "4  [John, Carter, is, a, war-weary,, former, mili...   \n",
       "\n",
       "                                         genres  \\\n",
       "0  [Action, Adventure, Fantasy, ScienceFiction]   \n",
       "1                  [Adventure, Fantasy, Action]   \n",
       "2                    [Action, Adventure, Crime]   \n",
       "3              [Action, Crime, Drama, Thriller]   \n",
       "4           [Action, Adventure, ScienceFiction]   \n",
       "\n",
       "                                            keywords  \\\n",
       "0  [cultureclash, future, spacewar, spacecolony, ...   \n",
       "1  [ocean, drugabuse, exoticisland, eastindiatrad...   \n",
       "2  [spy, basedonnovel, secretagent, sequel, mi6, ...   \n",
       "3  [dccomics, crimefighter, terrorist, secretiden...   \n",
       "4  [basedonnovel, mars, medallion, spacetravel, p...   \n",
       "\n",
       "                                            cast                crew  \n",
       "0  [SamWorthington, ZoeSaldana, SigourneyWeaver]      [JamesCameron]  \n",
       "1     [JohnnyDepp, OrlandoBloom, KeiraKnightley]     [GoreVerbinski]  \n",
       "2      [DanielCraig, ChristophWaltz, LéaSeydoux]         [SamMendes]  \n",
       "3      [ChristianBale, MichaelCaine, GaryOldman]  [ChristopherNolan]  \n",
       "4    [TaylorKitsch, LynnCollins, SamanthaMorton]     [AndrewStanton]  "
      ]
     },
     "execution_count": 185,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 186,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Concatinate all\n",
    "movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 187,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>movie_id</th>\n",
       "      <th>title</th>\n",
       "      <th>overview</th>\n",
       "      <th>genres</th>\n",
       "      <th>keywords</th>\n",
       "      <th>cast</th>\n",
       "      <th>crew</th>\n",
       "      <th>tags</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>19995</td>\n",
       "      <td>Avatar</td>\n",
       "      <td>[In, the, 22nd, century,, a, paraplegic, Marin...</td>\n",
       "      <td>[Action, Adventure, Fantasy, ScienceFiction]</td>\n",
       "      <td>[cultureclash, future, spacewar, spacecolony, ...</td>\n",
       "      <td>[SamWorthington, ZoeSaldana, SigourneyWeaver]</td>\n",
       "      <td>[JamesCameron]</td>\n",
       "      <td>[In, the, 22nd, century,, a, paraplegic, Marin...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>285</td>\n",
       "      <td>Pirates of the Caribbean: At World's End</td>\n",
       "      <td>[Captain, Barbossa,, long, believed, to, be, d...</td>\n",
       "      <td>[Adventure, Fantasy, Action]</td>\n",
       "      <td>[ocean, drugabuse, exoticisland, eastindiatrad...</td>\n",
       "      <td>[JohnnyDepp, OrlandoBloom, KeiraKnightley]</td>\n",
       "      <td>[GoreVerbinski]</td>\n",
       "      <td>[Captain, Barbossa,, long, believed, to, be, d...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>206647</td>\n",
       "      <td>Spectre</td>\n",
       "      <td>[A, cryptic, message, from, Bond’s, past, send...</td>\n",
       "      <td>[Action, Adventure, Crime]</td>\n",
       "      <td>[spy, basedonnovel, secretagent, sequel, mi6, ...</td>\n",
       "      <td>[DanielCraig, ChristophWaltz, LéaSeydoux]</td>\n",
       "      <td>[SamMendes]</td>\n",
       "      <td>[A, cryptic, message, from, Bond’s, past, send...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>49026</td>\n",
       "      <td>The Dark Knight Rises</td>\n",
       "      <td>[Following, the, death, of, District, Attorney...</td>\n",
       "      <td>[Action, Crime, Drama, Thriller]</td>\n",
       "      <td>[dccomics, crimefighter, terrorist, secretiden...</td>\n",
       "      <td>[ChristianBale, MichaelCaine, GaryOldman]</td>\n",
       "      <td>[ChristopherNolan]</td>\n",
       "      <td>[Following, the, death, of, District, Attorney...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>49529</td>\n",
       "      <td>John Carter</td>\n",
       "      <td>[John, Carter, is, a, war-weary,, former, mili...</td>\n",
       "      <td>[Action, Adventure, ScienceFiction]</td>\n",
       "      <td>[basedonnovel, mars, medallion, spacetravel, p...</td>\n",
       "      <td>[TaylorKitsch, LynnCollins, SamanthaMorton]</td>\n",
       "      <td>[AndrewStanton]</td>\n",
       "      <td>[John, Carter, is, a, war-weary,, former, mili...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   movie_id                                     title  \\\n",
       "0     19995                                    Avatar   \n",
       "1       285  Pirates of the Caribbean: At World's End   \n",
       "2    206647                                   Spectre   \n",
       "3     49026                     The Dark Knight Rises   \n",
       "4     49529                               John Carter   \n",
       "\n",
       "                                            overview  \\\n",
       "0  [In, the, 22nd, century,, a, paraplegic, Marin...   \n",
       "1  [Captain, Barbossa,, long, believed, to, be, d...   \n",
       "2  [A, cryptic, message, from, Bond’s, past, send...   \n",
       "3  [Following, the, death, of, District, Attorney...   \n",
       "4  [John, Carter, is, a, war-weary,, former, mili...   \n",
       "\n",
       "                                         genres  \\\n",
       "0  [Action, Adventure, Fantasy, ScienceFiction]   \n",
       "1                  [Adventure, Fantasy, Action]   \n",
       "2                    [Action, Adventure, Crime]   \n",
       "3              [Action, Crime, Drama, Thriller]   \n",
       "4           [Action, Adventure, ScienceFiction]   \n",
       "\n",
       "                                            keywords  \\\n",
       "0  [cultureclash, future, spacewar, spacecolony, ...   \n",
       "1  [ocean, drugabuse, exoticisland, eastindiatrad...   \n",
       "2  [spy, basedonnovel, secretagent, sequel, mi6, ...   \n",
       "3  [dccomics, crimefighter, terrorist, secretiden...   \n",
       "4  [basedonnovel, mars, medallion, spacetravel, p...   \n",
       "\n",
       "                                            cast                crew  \\\n",
       "0  [SamWorthington, ZoeSaldana, SigourneyWeaver]      [JamesCameron]   \n",
       "1     [JohnnyDepp, OrlandoBloom, KeiraKnightley]     [GoreVerbinski]   \n",
       "2      [DanielCraig, ChristophWaltz, LéaSeydoux]         [SamMendes]   \n",
       "3      [ChristianBale, MichaelCaine, GaryOldman]  [ChristopherNolan]   \n",
       "4    [TaylorKitsch, LynnCollins, SamanthaMorton]     [AndrewStanton]   \n",
       "\n",
       "                                                tags  \n",
       "0  [In, the, 22nd, century,, a, paraplegic, Marin...  \n",
       "1  [Captain, Barbossa,, long, believed, to, be, d...  \n",
       "2  [A, cryptic, message, from, Bond’s, past, send...  \n",
       "3  [Following, the, death, of, District, Attorney...  \n",
       "4  [John, Carter, is, a, war-weary,, former, mili...  "
      ]
     },
     "execution_count": 187,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 188,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['In',\n",
       " 'the',\n",
       " '22nd',\n",
       " 'century,',\n",
       " 'a',\n",
       " 'paraplegic',\n",
       " 'Marine',\n",
       " 'is',\n",
       " 'dispatched',\n",
       " 'to',\n",
       " 'the',\n",
       " 'moon',\n",
       " 'Pandora',\n",
       " 'on',\n",
       " 'a',\n",
       " 'unique',\n",
       " 'mission,',\n",
       " 'but',\n",
       " 'becomes',\n",
       " 'torn',\n",
       " 'between',\n",
       " 'following',\n",
       " 'orders',\n",
       " 'and',\n",
       " 'protecting',\n",
       " 'an',\n",
       " 'alien',\n",
       " 'civilization.',\n",
       " 'Action',\n",
       " 'Adventure',\n",
       " 'Fantasy',\n",
       " 'ScienceFiction',\n",
       " 'cultureclash',\n",
       " 'future',\n",
       " 'spacewar',\n",
       " 'spacecolony',\n",
       " 'society',\n",
       " 'spacetravel',\n",
       " 'futuristic',\n",
       " 'romance',\n",
       " 'space',\n",
       " 'alien',\n",
       " 'tribe',\n",
       " 'alienplanet',\n",
       " 'cgi',\n",
       " 'marine',\n",
       " 'soldier',\n",
       " 'battle',\n",
       " 'loveaffair',\n",
       " 'antiwar',\n",
       " 'powerrelations',\n",
       " 'mindandsoul',\n",
       " '3d',\n",
       " 'SamWorthington',\n",
       " 'ZoeSaldana',\n",
       " 'SigourneyWeaver',\n",
       " 'JamesCameron']"
      ]
     },
     "execution_count": 188,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "movies.iloc[0]['tags']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 189,
   "metadata": {},
   "outputs": [],
   "source": [
    "# droping those extra columns\n",
    "new_df = movies[['movie_id','title','tags']]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 190,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>movie_id</th>\n",
       "      <th>title</th>\n",
       "      <th>tags</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>19995</td>\n",
       "      <td>Avatar</td>\n",
       "      <td>[In, the, 22nd, century,, a, paraplegic, Marin...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>285</td>\n",
       "      <td>Pirates of the Caribbean: At World's End</td>\n",
       "      <td>[Captain, Barbossa,, long, believed, to, be, d...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>206647</td>\n",
       "      <td>Spectre</td>\n",
       "      <td>[A, cryptic, message, from, Bond’s, past, send...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>49026</td>\n",
       "      <td>The Dark Knight Rises</td>\n",
       "      <td>[Following, the, death, of, District, Attorney...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>49529</td>\n",
       "      <td>John Carter</td>\n",
       "      <td>[John, Carter, is, a, war-weary,, former, mili...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   movie_id                                     title  \\\n",
       "0     19995                                    Avatar   \n",
       "1       285  Pirates of the Caribbean: At World's End   \n",
       "2    206647                                   Spectre   \n",
       "3     49026                     The Dark Knight Rises   \n",
       "4     49529                               John Carter   \n",
       "\n",
       "                                                tags  \n",
       "0  [In, the, 22nd, century,, a, paraplegic, Marin...  \n",
       "1  [Captain, Barbossa,, long, believed, to, be, d...  \n",
       "2  [A, cryptic, message, from, Bond’s, past, send...  \n",
       "3  [Following, the, death, of, District, Attorney...  \n",
       "4  [John, Carter, is, a, war-weary,, former, mili...  "
      ]
     },
     "execution_count": 190,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "new_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 191,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "<ipython-input-191-a641d7570f8e>:2: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "  new_df['tags'] = new_df['tags'].apply(lambda x: \" \".join(x))\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>movie_id</th>\n",
       "      <th>title</th>\n",
       "      <th>tags</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>19995</td>\n",
       "      <td>Avatar</td>\n",
       "      <td>In the 22nd century, a paraplegic Marine is di...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>285</td>\n",
       "      <td>Pirates of the Caribbean: At World's End</td>\n",
       "      <td>Captain Barbossa, long believed to be dead, ha...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>206647</td>\n",
       "      <td>Spectre</td>\n",
       "      <td>A cryptic message from Bond’s past sends him o...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>49026</td>\n",
       "      <td>The Dark Knight Rises</td>\n",
       "      <td>Following the death of District Attorney Harve...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>49529</td>\n",
       "      <td>John Carter</td>\n",
       "      <td>John Carter is a war-weary, former military ca...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   movie_id                                     title  \\\n",
       "0     19995                                    Avatar   \n",
       "1       285  Pirates of the Caribbean: At World's End   \n",
       "2    206647                                   Spectre   \n",
       "3     49026                     The Dark Knight Rises   \n",
       "4     49529                               John Carter   \n",
       "\n",
       "                                                tags  \n",
       "0  In the 22nd century, a paraplegic Marine is di...  \n",
       "1  Captain Barbossa, long believed to be dead, ha...  \n",
       "2  A cryptic message from Bond’s past sends him o...  \n",
       "3  Following the death of District Attorney Harve...  \n",
       "4  John Carter is a war-weary, former military ca...  "
      ]
     },
     "execution_count": 191,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Converting list to str\n",
    "new_df['tags'] = new_df['tags'].apply(lambda x: \" \".join(x))\n",
    "new_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 192,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization. Action Adventure Fantasy ScienceFiction cultureclash future spacewar spacecolony society spacetravel futuristic romance space alien tribe alienplanet cgi marine soldier battle loveaffair antiwar powerrelations mindandsoul 3d SamWorthington ZoeSaldana SigourneyWeaver JamesCameron'"
      ]
     },
     "execution_count": 192,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "new_df.iloc[0]['tags']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 193,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "<ipython-input-193-9c6ff5dce70f>:2: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "  new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())\n"
     ]
    }
   ],
   "source": [
    "# Converting to lower case\n",
    "new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 194,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>movie_id</th>\n",
       "      <th>title</th>\n",
       "      <th>tags</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>19995</td>\n",
       "      <td>Avatar</td>\n",
       "      <td>in the 22nd century, a paraplegic marine is di...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>285</td>\n",
       "      <td>Pirates of the Caribbean: At World's End</td>\n",
       "      <td>captain barbossa, long believed to be dead, ha...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>206647</td>\n",
       "      <td>Spectre</td>\n",
       "      <td>a cryptic message from bond’s past sends him o...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>49026</td>\n",
       "      <td>The Dark Knight Rises</td>\n",
       "      <td>following the death of district attorney harve...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>49529</td>\n",
       "      <td>John Carter</td>\n",
       "      <td>john carter is a war-weary, former military ca...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   movie_id                                     title  \\\n",
       "0     19995                                    Avatar   \n",
       "1       285  Pirates of the Caribbean: At World's End   \n",
       "2    206647                                   Spectre   \n",
       "3     49026                     The Dark Knight Rises   \n",
       "4     49529                               John Carter   \n",
       "\n",
       "                                                tags  \n",
       "0  in the 22nd century, a paraplegic marine is di...  \n",
       "1  captain barbossa, long believed to be dead, ha...  \n",
       "2  a cryptic message from bond’s past sends him o...  \n",
       "3  following the death of district attorney harve...  \n",
       "4  john carter is a war-weary, former military ca...  "
      ]
     },
     "execution_count": 194,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "new_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 195,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'in the 22nd century, a paraplegic marine is dispatched to the moon pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization. action adventure fantasy sciencefiction cultureclash future spacewar spacecolony society spacetravel futuristic romance space alien tribe alienplanet cgi marine soldier battle loveaffair antiwar powerrelations mindandsoul 3d samworthington zoesaldana sigourneyweaver jamescameron'"
      ]
     },
     "execution_count": 195,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "new_df.iloc[0]['tags']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 196,
   "metadata": {},
   "outputs": [],
   "source": [
    "import nltk\n",
    "from nltk.stem import PorterStemmer"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 197,
   "metadata": {},
   "outputs": [],
   "source": [
    "ps = PorterStemmer()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 198,
   "metadata": {},
   "outputs": [],
   "source": [
    "def stems(text):\n",
    "    T = []\n",
    "    \n",
    "    for i in text.split():\n",
    "        T.append(ps.stem(i))\n",
    "    \n",
    "    return \" \".join(T)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 199,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "<ipython-input-199-ebce1bd97223>:1: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "  new_df['tags'] = new_df['tags'].apply(stems)\n"
     ]
    }
   ],
   "source": [
    "new_df['tags'] = new_df['tags'].apply(stems)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 200,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'in the 22nd century, a parapleg marin is dispatch to the moon pandora on a uniqu mission, but becom torn between follow order and protect an alien civilization. action adventur fantasi sciencefict cultureclash futur spacewar spacecoloni societi spacetravel futurist romanc space alien tribe alienplanet cgi marin soldier battl loveaffair antiwar powerrel mindandsoul 3d samworthington zoesaldana sigourneyweav jamescameron'"
      ]
     },
     "execution_count": 200,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "new_df.iloc[0]['tags']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 201,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.feature_extraction.text import CountVectorizer\n",
    "cv = CountVectorizer(max_features=5000,stop_words='english')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 202,
   "metadata": {},
   "outputs": [],
   "source": [
    "vector = cv.fit_transform(new_df['tags']).toarray()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 203,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([0, 0, 0, ..., 0, 0, 0], dtype=int64)"
      ]
     },
     "execution_count": 203,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "vector[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 204,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(4806, 5000)"
      ]
     },
     "execution_count": 204,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "vector.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 205,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "5000"
      ]
     },
     "execution_count": 205,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "len(cv.get_feature_names())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 207,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.metrics.pairwise import cosine_similarity"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 208,
   "metadata": {},
   "outputs": [],
   "source": [
    "similarity = cosine_similarity(vector)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 209,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(4806, 4806)"
      ]
     },
     "execution_count": 209,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "similarity.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 211,
   "metadata": {},
   "outputs": [],
   "source": [
    "# similarity"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 213,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "744"
      ]
     },
     "execution_count": 213,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "new_df[new_df['title'] == 'The Lego Movie'].index[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 214,
   "metadata": {},
   "outputs": [],
   "source": [
    "def recommend(movie):\n",
    "    index = new_df[new_df['title'] == movie].index[0]\n",
    "    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])\n",
    "    for i in distances[1:6]:\n",
    "        print(new_df.iloc[i[0]].title)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 219,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Spider-Man 3\n",
      "Spider-Man\n",
      "The Amazing Spider-Man\n",
      "Iron Man 2\n",
      "Superman\n"
     ]
    }
   ],
   "source": [
    "recommend('Spider-Man 2')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 221,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pickle"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 222,
   "metadata": {},
   "outputs": [],
   "source": [
    "pickle.dump(new_df,open('artifacts/movie_list.pkl','wb'))\n",
    "pickle.dump(similarity,open('artifacts/similarity.pkl','wb'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
