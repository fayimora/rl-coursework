class LinearFunction():
    features = [0 for i in range(18)]
    dealer_feature_template = [{1, 2, 3, 4}, {4, 5, 6, 7}, {7, 8, 9, 10}]
    player_feature_template = [
        {1, 2, 3, 4, 5, 6}, {4, 5, 6, 7, 8, 9},
        {7, 8, 9, 10, 11, 12}, {10, 11, 12, 13, 14, 15},
        {13, 14, 15, 16, 17, 18}, {16, 17, 18, 19, 20, 21}
    ]


    def get_features(self):
        return self.features


    def update(self, state):
        dealer, player = state.dealer, state.player
        dealer_feature, player_feature = [], []

        for i in range(len(self.dealer_feature_template)):
            if dealer in self.dealer_feature_template[i]:
                dealer_feature.append(1)
            else:
                dealer_feature.append(0)

        for i in range(len(self.player_feature_template)):
            if player in self.player_feature_template[i]:
                player_feature.append(1)
            else:
                player_feature.append(0)

        for i in range(len(self.features)):
            j = i // len(self.player_feature_template)
            k = i % len(self.player_feature_template)
            self.features[i] = dealer_feature[j] * player_feature[k]


